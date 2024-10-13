# Dictation File Generator

A Flask-based web application that allows users to create PowerPoint presentations from text input. Users can enter text directly or upload a file, and the application generates a PPTX file using a modular core library for enhanced functionality. The project emphasizes code separation, modularity, and robust error handling, making it suitable for educational and professional use. It also includes features for emailing generated presentations and validating user input.

This project converts text files into PowerPoint slides, focusing on dictation-style formatting. The project uses the core.file.generator library to modularize the PowerPoint generation, handling tasks such as slide creation, text box addition, and header/footer formatting. Key features include:

- Dynamic word-based text box creation.
- Customizable styles via JSON.
- Automated slide layout handling for text overflow.