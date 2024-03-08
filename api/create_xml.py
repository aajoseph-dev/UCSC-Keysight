from xml.dom import minidom 
import os

def create_xml(name, py_file):

    # Initialize document called doc
    doc = minidom.Document() 
    
    # Create root element <Package>
    package = doc.createElement('Package')  
    doc.appendChild(package)

    # Set attributes for <Package>
    package.setAttribute('Name', name) 
    package.setAttribute('xmlns', "http://keysight.com/Schemas/tap") 
    package.setAttribute('Version', "$(GitVersion)") 
    package.setAttribute('OS', "Windows,Linux,MacOS") 

    # Create child element <Description>
    des = doc.createElement('Description')
    package.appendChild(des)
    
    # Add text to description
    des_text = doc.createTextNode('TEST')
    des.appendChild(des_text)

    # Create child element <Prerequisites>
    prereq = doc.createElement('Prerequisites')
    des.appendChild(prereq)
    prereq_text = doc.createTextNode(' Python (>3.7) ')
    prereq.appendChild(prereq_text)

    # Create child element <Files>
    files = doc.createElement('Files')
    package.appendChild(files)

    # Create child element <File>
    py = doc.createElement('File')
    py.setAttribute('Path', py_file)
    files.appendChild(py)

    # Create end tag for project file
    end_project_file = doc.createElement('ProjectFile')
    py.appendChild(end_project_file) 

    # Generate the xml string
    xml_str = doc.toprettyxml(indent ="\t", encoding="UTF-8")  
  
    # XML file name created in the same direction as where the create_xml.py is ran
    save_path_file = "new_xml.xml"
    
    # Save the xml file in binary
    with open(save_path_file, "wb") as f: 
        f.write(xml_str) 




if __name__ == "__main__":
    create_xml("TEST", "C:/Projects/TEST/TEST/*.py")