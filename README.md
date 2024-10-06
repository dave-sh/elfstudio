# ELFStudio

ELF binary static analysis tool written in Python designed for Linux machines.

This is a project I decided to build that was inspired by a popular windows program used to statically analyze PE files. I had the basic idea of this after taking a cybersecurity course. For an assignment, I had to set up logging to detect file system changes caused by a ELF malware sample, but was unable to find it due to a bug in the binary. To combat this, I decided to see if I could reverse engineer the binary and uncover the intended behavior through static analysis. I included some features in this program that were helpful to me in determining the function of the binary. It's by no means as sophisticated as a proper disassembler but I thought it might be helpful to other people in the future. 

Essentially, this serves as a graphical wrapper for a lot of built-in Linux system command line utilities. Any suggestions would be appreciated. 

### Current Feature Set
- Detect File Signature, hash, and other basic information.
- Display program strings.
- Display information on exports, imports, and linked libraries.

### Planned Feature Set
- Retrieve VirusTotal information (feature in development)
- Export to txt/csv (feature in development)

### Basic Usage
![image](https://github.com/user-attachments/assets/f5d7f251-e147-45c7-86b4-e35163e31041)

![image](https://github.com/user-attachments/assets/cb3db7e3-991e-4c6a-bc7f-12b18c06c811)

![image](https://github.com/user-attachments/assets/2d7e8305-fe15-4bf5-b397-45969ef5021a)

![image](https://github.com/user-attachments/assets/7beb5fa5-27c7-43f2-8096-49c84d512e3c)

![image](https://github.com/user-attachments/assets/7218255a-6762-4ec6-ac34-a2f452732358)


