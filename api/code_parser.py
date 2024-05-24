import ast
from nltk.sentiment.vader import SentimentIntensityAnalyzer

#code_parser defines functions used within app.py to help vaidalte code 
#primiarly throught the use of abstract sytnax tree

def instrument_validation(code):

    verification_results = ''
    has_opentap_import = False
    has_OpenTap_import = False
    has_correct_inheritance = False
    has_correct_decorator = False
    has_init_method = False
    has_super_call = False

    tree = ast.parse(code)


    for node in ast.walk(tree):
        if isinstance(node, ast.ImportFrom):
            if node.module == 'opentap' and any(alias.name == '*' for alias in node.names):
                has_opentap_import = True

        if isinstance(node, ast.Import):
            for alias in node.names:
                if alias.name == 'OpenTap':
                    has_OpenTap_import = True

        if isinstance(node, ast.ImportFrom):
            if node.module == 'opentap' and any(alias.name == '*' for alias in node.names):
                has_opentap_import = True

        if isinstance(node, ast.ClassDef):
            for base in node.bases:
                if isinstance(base, ast.Attribute):
                    if (base.attr == 'ScpiInstrument' and isinstance(base.value, ast.Name) and base.value.id == 'OpenTap'):
                        has_correct_inheritance = True
        
            for decorator in node.decorator_list:
                if isinstance(decorator, ast.Call):
                    if isinstance(decorator.func, ast.Name) and decorator.func.id == 'attribute':
                        if len(decorator.args) == 1 and isinstance(decorator.args[0], ast.Call):
                            inner_call = decorator.args[0]
                            if isinstance(inner_call.func, ast.Attribute):
                                if inner_call.func.attr == 'Display' and isinstance(inner_call.func.value, ast.Name) and inner_call.func.value.id == 'OpenTap':
                                    has_correct_decorator = True
            for body_node in node.body:
                if isinstance(body_node, ast.FunctionDef) and body_node.name == '__init__':
                    has_init_method = True
                    for expr in body_node.body:
                        if isinstance(expr, ast.Expr) and isinstance(expr.value, ast.Call):
                            if isinstance(expr.value.func, ast.Attribute):
                                if expr.value.func.attr == '__init__' and isinstance(expr.value.func.value, ast.Call):
                                    if isinstance(expr.value.func.value.func, ast.Name) and expr.value.func.value.func.id == 'super':
                                        if isinstance(expr.value.func.value.args[0], ast.Name) and expr.value.func.value.args[0].id == node.name:
                                            has_super_call = True

    if not has_opentap_import:
        verification_results += "The import 'from opentap import *' is not present.\n"
        code = "from opentap import *\n" + code 
    if not has_OpenTap_import:
        verification_results += "The import 'import OpenTap' is not present.\n"
        code = "import OpenTap\n" + code
    if not has_correct_inheritance:
        verification_results += "No class inherits from 'OpenTap.ScpiInstrument' or 'ScpiInstrument'.\n"
    if not has_correct_decorator:
        verification_results += "No class has the correct @attribute(OpenTap.Display) decorator.\n"
    if not has_init_method:
        verification_results += "No __init__ method found in the class.\n"
    if not has_super_call:
        verification_results += "No call to super(<classname>, self).__init__() found in the __init__ method.\n"

    return verification_results, code


def test_step_validation(code):

    verification_results = ''
    has_opentap_import = False
    has_OpenTap_import = False
    has_correct_inheritance = False
    has_init_method = False
    has_run_method = False
    has_super_call = False

    tree = ast.parse(code)

    for node in ast.walk(tree):
        if isinstance(node, ast.ImportFrom):
            if node.module == 'opentap' and any(alias.name == '*' for alias in node.names):
                has_opentap_import = True

        if isinstance(node, ast.Import):
            for alias in node.names:
                if alias.name == 'OpenTap':
                    has_OpenTap_import = True

        if isinstance(node, ast.ClassDef):
            for base in node.bases:
                if isinstance(base, ast.Name) and base.id == 'TestStep':
                    has_correct_inheritance = True

            for body_node in node.body:
                if isinstance(body_node, ast.FunctionDef):
                    if body_node.name == '__init__':
                        has_init_method = True
                        for expr in body_node.body:
                            if isinstance(expr, ast.Expr) and isinstance(expr.value, ast.Call):
                                if isinstance(expr.value.func, ast.Attribute):
                                    if expr.value.func.attr == '__init__' and isinstance(expr.value.func.value, ast.Call):
                                        if isinstance(expr.value.func.value.func, ast.Name) and expr.value.func.value.func.id == 'super':
                                            if isinstance(expr.value.func.value.args[0], ast.Name) and expr.value.func.value.args[0].id == node.name:
                                                has_super_call = True
                    elif body_node.name == 'Run':
                        has_run_method = True
                        for expr in body_node.body:
                            if isinstance(expr, ast.Expr) and isinstance(expr.value, ast.Call):
                                if isinstance(expr.value.func, ast.Attribute):
                                    if expr.value.func.attr == 'Run':
                                        has_run_method = True
                                        if isinstance(expr.value.func.value, ast.Call):
                                            if isinstance(expr.value.func.value.func, ast.Name) and expr.value.func.value.func.id == 'super':
                                                has_super_call = True

    if not has_opentap_import:
        verification_results += "The import 'from opentap import *' is not present.\n"
        code = "from opentap import *\n" + code 
    if not has_OpenTap_import:
        verification_results += "The import 'import OpenTap' is not present.\n"
        code = "import OpenTap\n" + code
    if not has_correct_inheritance:
        verification_results += "No class inherits 'TestStep'.\n"
    if not has_init_method:
        verification_results += "No __init__ method found in the class.\n"
    if not has_run_method:
        verification_results += "No 'Run' method found in the class.\n"
    if not has_super_call:
        verification_results += "No call to 'super().Run()' found within the 'Run' method.\n"

    return verification_results, code


def extract_python_code(text):

    start_index = text.find("```python")
    end_index = text.find("```", start_index + 1)

    if start_index != -1 and end_index != -1:
        text = text[start_index + 9:end_index].strip()

    return text

def sentiment_analysis(content):

    sid = SentimentIntensityAnalyzer()

    scores = sid.polarity_scores(content)

    if scores['compound'] <= -0.25: 
        return {"Sentiment" : "Negative", "Response" : content}
    
    return {"Sentiment" : "Positive", "Response" : content}