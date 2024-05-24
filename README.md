# UCSC-Keysight
Using generative AI to automate plugin generation to connect to Keysight's OpenTAP.

## Getting Started:
To utilize this automated plugin generation tool, follow these steps:

1. Clone the repo.
2. Open VS Code.
3. In two separate VS Code terminal create and activate a virutal environment by running: ```python3 -m venv .venv``` and then ```source .venv/bin/activate```.
5. In a VS Code terminal run: ```pip install -r requirements.txt```
6. Run python3 app.py in one terminal to start the server.
7. Run python3 client.py to start the client application to get the popup window to appear.
8. Enter in your device specs into the popup window.
9. Wait for the program to generate your plugin.
10. Plugin gets saved into the location that you specified in the popup window.

## Terminology
* **OpenTAP** - Keysight’s open source test automation project that automates standardized testing for devices, such as power supplies and batteries.
* **Plugin** - Software used to communicate between OpenTAP and the instrument being tested. Need a different plugin to connect to OpenTAP for every instrument.
* **LLM** - Large Language Model is a type of AI program that can recognize and generate text; e.g. ChatGPT.
* **RAG** Approach - Retrieval Augmented Generation. Uses external data sources, such as instrument documents, to provide context that the LLM uses to base its answer on.

## Overview:
* Test engineers, who do not necessarily have a software background, spend time learning how to create a new plugin for every device they want to test.
* We leverage LLMs to create and verify plugins for user-specified devices to minimize development time so that test engineers can focus on testing rather than initially developing software plugins.

## Abstract:
* Targeting test engineers involved in test automation, our AI-based solution offers an innovative approach to streamline plugin creation.
* We utilize LLMs to create a plugin for a user-specified device in Python or C#, decreasing software development time for test engineers.
* A common problem when AI is involved is AI hallucinations (incorrect or misleading results that AI models generate), which we reduced by implementing the RAG approach.

## Key Features:
- **Generative AI Plugin Generator**: Utilizes cutting-edge Generative AI algorithms, powered by LLM GPT-4, to automatically generate plugin code based on user-defined specifications.
- **Python PYQT5 Intetface**: The user-friendly WPF (Windows Presentation Foundation) interface provides an intuitive environment for configuring plugin parameters and generating code.
- **Azure AI Search Integration**: Harnesses the power of Azure AI Search to enhance code generation accuracy and efficiency.
- **LangChain Support**: Integrates LangChain for multi-language support, enabling code generation in various programming languages.

## How it Works:
1. **Input Specifications**: Users provide input parameters and requirements for the desired plugin via the WPF interface.
2. **Generative AI Processing**: The system processes user inputs using Generative AI algorithms to generate code snippets tailored to the specifications.
3. **Code Generation**: Generated code snippets are assembled into complete plugin code structures in Python.
4. **Output & Integration**: Users can review and integrate the generated code directly into their OpenTAP projects, significantly reducing manual coding efforts by a ~70% decrease.

<img width="1003" alt="Screenshot 2024-05-13 at 3 20 01 PM" src="https://github.com/aajoseph-dev/UCSC-Keysight/assets/92142459/a57ea050-272b-4671-bc5a-88e12da39377">

## Technologies Used:
1. **Frontend**: Python PyQt5 - Popup window that receives user input.
2. **LLMs**: OpenAI’s GPT-4 - Generates and verifies the plugin code.
3. **Server**: Flask - Runs a server that makes calls to Azure AI Search and the LLMs.
4. **Database**: Azure AI Search - Queries the database based on keywords found in user’s input.
5. **PDF handling**: LangChain - Chunks and vectorizes the PDFs, uploads them to AI Search’s database.

<img width="1003" alt="Screenshot 2024-05-13 at 3 21 24 PM" src="https://github.com/aajoseph-dev/UCSC-Keysight/assets/92142459/3de8ba28-8ea4-4660-9127-a6d31e259950">

<img width="1088" alt="Screenshot 2024-05-13 at 3 25 11 PM" src="https://github.com/aajoseph-dev/UCSC-Keysight/assets/92142459/07764237-1e78-4711-8af5-484c8133fc30">

## Analysis:
* When comparing the time it takes for a developer to code a plugin from scratch versus time spent waiting for a plugin to be generated, we found that we reduced the development time of OpenTap plugins by **~70%**.
* In evaluating the accuracy of code generation, we examined whether the generated code meets syntactical requirements, adheres to the coding structure of plugins, and complies with errors.

## Results:
* **Plugin Generation**: Successfully generates plugins for a wide range of Keysight tools based on user’s device specifications by leveraging LLM models and the RAG approach. 
* **Streamlined Verification**: Plugins are verified before they are sent back to the use, ensuring that they compile and the necessary structural elements.
* **Compatibility Assurance**: Plugins produced can be used directly with various keysight softwares without any additional modifications.

## Conclusion
* We were able to decrease development time so that test engineers can focus on testing their device rather than software development.
* In the future, more time can be spent on fine tuning the prompt passed to the LLMs to produce the most accurate plugin.
* Additionally, the database that the LLMs have access to can be expanded with more extensive documentation to increase the quality of plugins that are produced.

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
