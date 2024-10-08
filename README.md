# ELFStudio

**ELF Studio** is a static analysis tool for ELF binaries, developed in Python specifically for Linux environments.

This project was inspired by a well-known Windows application for analyzing PE files. The initial concept emerged from my experience in a cybersecurity course where I needed to implement logging to detect filesystem changes triggered by an ELF malware sample. Unfortunately, I encountered a bug in the binary that hindered my progress. To address this challenge, I set out to reverse engineer the binary and uncover its intended behavior through static analysis. This tool includes various features that proved beneficial for analyzing the binary's functionality and serves as a graphical interface for several command-line utilities. While it may not be as advanced as a full-fledged disassembler, I believe it offers a valuable exploration into ELF binaries.

### Current Feature Set
- Detects file signatures, hashes, and other fundamental information.
- Displays program strings.
- Provides information on exports, imports, and linked libraries.

### Planned Feature Set
- Integration with VirusTotal (feature in development).
- Export options to TXT/CSV (feature in development).

### Basic Usage

![Screenshot of ELF Studio in action](https://github.com/user-attachments/assets/f5d7f251-e147-45c7-86b4-e35163e31041)

![Detailed analysis view in ELF Studio](https://github.com/user-attachments/assets/cb3db7e3-991e-4c6a-bc7f-12b18c06c811)

![User interface showing program strings](https://github.com/user-attachments/assets/2d7e8305-fe15-4bf5-b397-45969ef5021a)
