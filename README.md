# crawl-classes

RPI has an *amazing* variety of courses, but this makes its course catalog very long and tedious to navigate. It would be much easier to visualize the prerequisites of each course using a graph!
This project includes all of the tools which are necessary to produce such a graph, so that RPI students can see a **clear course progression** for their major:

- Web scraping the catalog using Python's 'requests' and 'beautifulSoup4' libraries
- Storing cached versions of the online html pages so that re-running the program doesn't cause extra burden on RPI servers
- Instantiating Course objects for each course in the catalog
- Writing the catalog (a Python dictionary) to a pickled file for later use
- Converting the Python dictionary of courses to a '.dot' file for graph display
- Using dot's command line interface (dot -Ktwopi -o <output_file.type> -T<image type> <file.dot>) to generate an image from the .dot file

Here's a sample output of all courses in the RPI catalog with prerequisites: ![prereqs graph](rpidot.png)

Here's an interesting graph of Computer Science departement courses at RPI: ![cs graph](cs_only.png)
