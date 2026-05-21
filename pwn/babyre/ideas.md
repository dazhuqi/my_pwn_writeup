# Easy_re Writeup
Link to the question: https://ctf.bugku.com/challenges/detail/id/99.html

## Overview
Unzip the download zip. Then check the file feature
![file_exp.png](screenshots/file_exp.png)

Use Ghidra to open this file, then search ``main`` function.<br>
You will see the "odd" code segment, transfer it you can get flag.

![flag.png](screenshots/flag.png)