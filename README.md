# Background

A big part of the lab manager's job will be to write scripts that facilitate data collection, annotation, and analysis. This technical task is meant to give you an idea of the type of work involved in prepping data for analysis.

When RAs manually annotate data in the lab, they may use one of several applications, depending on the type of data (e.g., Excel/Google Spreadsheets, Praat, ELAN, Datavyu, etc.). When it comes to doing analysis, however, we need to get their annotations into a text-based tabular format. Usually this can be done by hand within each application (e.g., via some specialized export function) but it's often much quicker and less error-prone to do this re-formatting automatically.

I have provided you here with an .eaf file. This file type is used in the application [ELAN](https://archive.mpi.nl/tla/elan) and, underlyingly, it is just XML. I am also providing you with an example of a tab-delimited text file. The text file features a few of the key fields that we typically use for analysis with transcribed data. I created the text file by exporting it manually in the ELAN environment and selecting a subset of the output options, as shown here.

![ELAN manual export example](ELAN_manual_export_example.png)

## Task summary

Your task is to create a tool that takes, as input, an .eaf file (structured as in the example) and gives, as output, a .txt file (structured as in the example). The output file should appear next to the input file in the same directory by default, and with the same basename as the input file. You can accomplish this task in up to three ways:

### Level 1: Command-line script, input path as argument

Provide me with a program and associated code for running this tool at the command line. Your tool should:

* Take an input path as an argument,
* Provide usage info for the argument (and any flags you create), and
* Be able to run over single files or batches of files, e.g., at input `PATH/*.eaf`

Note: Use R or Python, as you like.

_Why this level?_ More advanced students and researchers who want to reuse our lab's open-source code are likely to be comfortable running scripts at the command line, often finding this more convenient than having to hand-edit a script in order to adjust it to their requirements.

### Level 2: 
Modify the code to produce output listed chronologically by chronological ordering and  `@` tiers below the main tiers.

* Modify your code to output the list by chronological ordering. The ordering should be based on the start and end times, in that order.
* In addition, your code should output subtier lines (lines that start with lower case `vcm@`, `xds@` or `lex@`) below the main tier lines. For example: 

```
CHI	CHI	1740	2994	1254	0.
vcm@CHI	CHI	1740	2994	1254	C
lex@CHI	CHI	1740	2994	1254	0

```


### Level 3:

Modify your code to output a couple of summary data:

* Which speaker had the most turns?
* Which speaker talked the most (cumulatively)? 
* Which speaker had the most **non-speaking** turns (where instead of any annotations, there is only `0.`)?



## Submission

Please share with me a GitHub repo in which you have stored your code. If you are doing level 3, you can either just have me run the app myself locally using `shiny::runApp()` or you can host it and send me a URL (up to you). Indicate in the README of your repo which level you have aimed at. I have a collection of other files similar to the example one that I will use to test your tool. I'm on a Mac so whatever you do to mitigate my needing to install things/change paths (e.g., from back- to forward-slash) is appreciated :)

## Evaluation

The goal is not to test whether you can do all these things, but just to evaluate what your current comfort level is—do not feel compelled to do level 3 by default! Instead, choose the level that most suits your current skills and available time between now and Monday night. I will be looking at your code style, commenting, tests, edge case handling, README clarity, etc. Your task should run successfully and be tidily documented in line with your current best ability. Quality counts over quantity/level number.

Resourcefulness is a virtue! Feel free to use existing packages  that might make this task simpler. You may also find solutions posted for similar tasks—great! Just please clearly cite any code you re-use.

Last but not least, I'd appreciate it if you kept your full revision history for this project in the Github repo. I won't go snooping deep into your history so don't be bashful. I just want to get a sense for how you chunk your commits and what your messages are like.
