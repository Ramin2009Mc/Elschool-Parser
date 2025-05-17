# 📚 Elschool parser

> Effortlessly extract, analyze, and visualize your grades and homework from Elschool.ru ✨

---
![Python](https://img.shields.io/badge/Python-3.11-blue?logo=python&logoColor=white) ![Email](https://img.shields.io/badge/raminkiyamov@gmail.com-blue?logo=gmail&logoColor=white)



## 🚀 Features

- 🔐 **Secure login**: Enter your credentials at runtime, nothing is stored in code.
- 📊 **Grades parsing**: Instantly fetch your full report card, including all subjects and quarters.
- 📝 **Homework extraction**: View all your homework assignments, organized by day and subject.
- 📈 **Excel export**: Save your grades to a beautifully formatted Excel file with a single click.
- 🎨 **Modern CLI**: Enjoy a stylish, interactive terminal interface powered by [rich](https://github.com/Textualize/rich).
- 🦾 **Fast & reliable**: Built with robust error handling and clear feedback for every action.

---

## 🖥️ Quick Start

### 1. Clone the repository
```bash
git clone https://github.com/yourusername/ElschoolParser.git
cd ElschoolParser
```

### 2. Create and activate a virtual environment (recommended)
```bash
python3 -m venv env
source env/bin/activate
```

### 3. Install dependencies
```bash
pip install -r requirements.txt
```

### 4. Run the parser

```bash
python main.py
```

---

## 🧑‍💻 Usage

When you start the program, you'll see a beautiful ASCII-art welcome and a menu:

```
1. View the report card (grades)
2. View your homework
3. Save the report card (grades) to an Excel file
0. Exit
```

- **View the report card**: See all your subjects, average scores, and grades by quarter.
- **View your homework**: Get a day-by-day breakdown of all homework assignments.
- **Save to Excel**: Export your grades to `marks/<your_login>_marks.xlsx` for easy sharing and analysis.

---

## 🛠️ Requirements
- Python 3.8+
- See `requirements.txt` for all Python dependencies

---

## ⚡ Example

```bash
$ python main.py

             .--.           .---.        .-.
         .---|--|   .-.     | R |  .---. |~|    .--.
      .--|===|Sa|---|_|--.__| A |--|:::| |~|-==-|==|---.
      |%%|✩₊˚|cu|===| |~~|%%| M |--|   |_|~|CATS|  |___|-.
      |  |⊹𓂃|ra|===| |==|  | I |  |:::|=| |    |IT|---|=|
      |  | ✮ |  |   |_|__|  | N |__|   | | |    |  |___| |
      |~~|===|--|===|~|~~|%%|~~~|--|:::|=|~|----|==|---|=|
      ^--^---'--^---^-^--^--^---'--^---^-^-^-==-^--^---^-'

Welcome to Elschool!

Enter login: <your_login>
Enter password: <your_password>

Menu:
1. View the report card (grades)
2. View your homework
3. Save the report card (grades) to an Excel file
0. Exit
```

---

## 📂 Output Example
- Grades Excel file: `marks/<your_login>_marks.xlsx`

---

## ❓ FAQ

**Q: Are my credentials safe?**
- Yes! Your login and password are only used for the session and are never saved to disk.

**Q: What if I get an error?**
- The app will show a friendly message. Check your credentials and internet connection, then try again.

---

## ☝🏻 Helpful links
- [Python documentation](https://docs.python.org/3.11/)
- [Beatiful soup documentation](https://beautiful-soup-4.readthedocs.io/en/latest/)
- [Requests documentation](https://requests.readthedocs.io/en/latest/index.html)
- [Rich documentation](https://rich.readthedocs.io/en/stable/)

## Author 👨🏻‍💻
Created by Ramin Kiyamov
📧 Email: raminkiyamov@gmail.com

---
