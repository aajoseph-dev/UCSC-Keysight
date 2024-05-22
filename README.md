## About The Project

<p align="center">
    <img src="/assets/project-screenshot.png" alt="Alt text" width="500" />
</p>


This project leverages Azure AI Search and Large Language Models (LLMs) to automate the creation of OpenTAP plugins, ensuring they meet specific requirements and standards. By integrating advanced AI capabilities, the tool helps reduce development time while maintaining adherence to OpenTAP standards.

## Built With
[![Azure AI Search](https://img.shields.io/badge/Azure%20AI%20Search-0078D4?style=for-the-badge&logo=microsoft&logoColor=white)](https://azure.microsoft.com/en-us/services/search/)
[![OpenAI](https://img.shields.io/badge/OpenAI-412991?style=for-the-badge&logo=openai&logoColor=white)](https://www.openai.com/)
[![OpenTAP](https://img.shields.io/badge/OpenTAP-FF6F61?style=for-the-badge&logo=openstack&logoColor=white)](https://opentap.io/)
[![Flask](https://img.shields.io/badge/Flask-000000?style=for-the-badge&logo=flask&logoColor=white)](https://flask.palletsprojects.com/)
[![PyQt6](https://img.shields.io/badge/PyQt6-41CD52?style=for-the-badge&logo=qt&logoColor=white)](https://riverbankcomputing.com/software/pyqt/intro)


## Getting Started

### Prerequisites
Before getting started, ensure you have the following prerequisites installed:
- Python 3.x
- pip package manager

### Installation
To utilize this automated plugin generation tool, follow these steps:

1. **Clone the repository:**
    ```bash
    git clone git@github.com:aajoseph-dev/UCSC-Keysight.git
    cd UCSC-Keysight
    ```

2. **Set up a virtual environment:**
    ```bash
    python3 -m venv .venv
    source .venv/bin/activate
    ```

3. **Install dependencies:**
    ```bash
    pip install -r requirements.txt
    ```

4. **Start the server:** 
    In the api directory run
   ```bash
    python app.py
    ```

6. **Start the client:**
    In the client directory run
    ```bash
    python client.py
    ```

7. **Enter device information:**
    In the UI, enter the required device information.

8. **Generate the plugin:**
    Click the "Generate" button and wait for the program to create your plugin.

9. **Unzip the plugin:**
    Once generated, the plugin will be returned as a zip folder. Unzip the file.

10. **Create package.xml:**
    Run the following command to create the package.xml file:
    ```bash
    tap package create package.xml
    ```

## Usage



## Acknowledgements

Developed in collaboration with the University of California, Santa Cruz (UCSC) and Keysight Technologies through the Corporate Sponspored Senior Projects Program (CSSPP).

**Keysight**: Jeff Dralla, Maxim Pletner, Alan Copeland, Brennen Direnzo, Ivan Diep

**UCSC**: Richard Jullig, Prajas Kadepurkar

## Authors

- **Ahmad Joseph** - [aajoseph-dev](https://github.com/aajoseph-dev)
- **Madeline Miller** - [MadelineMiller](https://github.com/MadelineMiller)
- **Shaunveer Gill** - [ShaunveerGill](https://github.com/ShaunveerGill)
- **Huy Nguyen** - [huy-nguy3n](https://github.com/huy-nguy3n)
- **Philip Xie** - [pjxie](https://github.com/pjxie)


