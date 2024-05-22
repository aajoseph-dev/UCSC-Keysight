import ast
import time

class code_parsing():
    def test_instrument_validation(code):
        start_time = time.time()
        
        # Parse the code into an abstract syntax tree
        tree = ast.parse(code)

        # Initialize verification result
        verification_result = ''

        # Check for function and class definitions
        has_function_or_class = any(isinstance(node, (ast.FunctionDef, ast.ClassDef)) for node in ast.walk(tree))
        if has_function_or_class:
            verification_result += 'Found class and function definitions.'
        else:
            verification_result += 'Unable to find class and function definitions.'

        # Check for OpenTAP import
        has_opentap_import = any(isinstance(node, ast.Import) and any(alias.name == 'OpenTAP' for alias in node.names) for node in tree.body)
        if not has_opentap_import:
            # Adding OpenTAP import if not present
            code = 'import OpenTAP\n' + code

        # Check for opentap import
        has_opentap_import_lowercase = any(isinstance(node, ast.Import) and any(alias.name == 'opentap' for alias in node.names) for node in tree.body)
        if not has_opentap_import_lowercase:
            code = 'import opentap\n' + code

        # Check for @attribute
        has_attribute_annotation = any(isinstance(node, ast.FunctionDef) and any(isinstance(dec, ast.Name) and dec.id == 'attribute' for dec in node.decorator_list) for node in ast.walk(tree))
        if has_attribute_annotation:
            verification_result += ' Found @attribute.'
        else:
            verification_result += ' @attribute not found.'

        # Check for class definitions
        for node in tree.body:
            if isinstance(node, ast.ClassDef):
                # Check if the class inherits from OpenTap.ScpiInstrument
                if any(isinstance(base, ast.Attribute) and base.value.id == 'OpenTap' and base.attr == 'ScpiInstrument' for base in node.bases):
                    verification_result += f"Class {node.name} inherits from OpenTap.ScpiInstrument.\n"
                else:
                    verification_result += f"Class {node.name} does not inherit from OpenTap.ScpiInstrument.\n"
        
        time_ast = time.time() - start_time
        return time_ast

    def test_step_validation(code):
        start_time = time.time()
        
        # Parse the code into an abstract syntax tree
        tree = ast.parse(code)

        # Initialize verification result
        verification_result = ''

        # Check for class definitions
        for node in tree.body:
            if isinstance(node, ast.ClassDef):
                # Check if the class inherits from TestStep
                inherits_teststep = any(isinstance(base, ast.Attribute) and base.value.id == 'TestStep' for base in node.bases)
                
                # Check if the class has @attribute(OpenTap.Display())
                has_opentap_display = False
                for decorator in node.decorator_list:
                    if isinstance(decorator, ast.Call) and isinstance(decorator.func, ast.Attribute) and decorator.func.attr == 'attribute':
                        for keyword in decorator.keywords:
                            if keyword.arg == 'display' and isinstance(keyword.value, ast.Call) and isinstance(keyword.value.func, ast.Attribute) and keyword.value.func.value.id == 'OpenTap' and keyword.value.func.attr == 'Display':
                                has_opentap_display = True
                                break
                
                # Check for __init__ method
                has_init_method = any(isinstance(elt, ast.FunctionDef) and elt.name == '__init__' for elt in node.body)
                
                # Check for Run method
                has_run_method = any(isinstance(elt, ast.FunctionDef) and elt.name == 'Run' for elt in node.body)
                
                # Check if there are no other methods besides __init__ and Run
                other_methods = [elt.name for elt in node.body if isinstance(elt, ast.FunctionDef) and elt.name not in ('__init__', 'Run')]
                
                if inherits_teststep and has_opentap_display and has_init_method and has_run_method and not other_methods:
                    verification_result += f"Class {node.name} meets all criteria.\n"
                else:
                    verification_result += f"Class {node.name} does not meet all criteria.\n"

        end_time = time.time()
        return end_time - start_time

# Test the AST-based approach
time_ast = test_instrument_validation(code)

print("Time taken for AST-based approach:", time_ast)
