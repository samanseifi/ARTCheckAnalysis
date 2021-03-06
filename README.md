# ARTCheckAnalysis

This is the script to analyse the ART output from the CDM code (a.k.a `ARTRollOut.xls`). It gives out two separate `txt` files one shows checks either passed or failed `check_summary_passfail_<DEMSTR>.txt` and the other shows the numerical outputs `check_summary_numerics_<DEMSTR>.txt`. Also it generates the plots showing the outcome of simulation between 2014 and 2019 and compare to baseline data. The `<DEMSTR>` is a suffix for racial demography of interest.

An example of running the script:

`python3 art-checks.py <year> <time_step> <path_to_excel> <demographic_type>`

`<year>`: is the delayed prevalence year when initial infections were seeded. e.g. 2007

`<time_step>`: is the corresponding time step to the delayed prevalence year.

`<path_to_excel>`: this is the path to the directory for the script to search for `ARTRollOut.xls` files. It will find all the excel files in subdirectories as well.

`<demographic_type>`: this is to process data of a certain racial demography. Options are: `WHITE`, `BLACK`, `HISPANIC` and `OTHER`. For total population use `TOTAL`.

and example of the script for MAMI analysis is:

`python3 art-checks.py 2007 600 . WHITE`