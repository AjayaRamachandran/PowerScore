ending = '''
        <div class="gap-2">
            <div class="gap-2"></div>
        </div>
        <div class="gap-2">
            <div class="gap-2"></div>
        </div>
    </div>
    <div class="bottom">
        © Copyright 2024 by Ajaya Ramachandran, Team 8568A 23-24
        <div class="bottom-bottom">
            <div class="v-gap-2">
                <div class="v-gap-2"></div>
            </div>
            <div class="v-gap-2">
                <div class="v-gap-2"></div>
            </div>
            <div class="bottom-column">
                <div class="bottom-column-item"><a target="_blank" href="https://forms.gle/uv3X3gEELeUg8D2L6">Improve This Site</a></div>
                <div class="bottom-column-item"><a target="_blank" href="mailto:na8568a@gmail.com">Contact Us</a></div>
                <div class="bottom-column-item"><a target="_blank" href="https://github.com/AjayaRamachandran">Support Me on GitHub</a></div>
                <div class="bottom-column-item"><a target="_blank" href="https://drive.google.com/file/d/1NEs-AuhDzaLs1RFFhTsF3nnK5rGLdCWZ/view?usp=sharing">Credits</a></div>
            </div>
            <div class="bigger-gap-2">
                <div class="bigger-gap-2"></div>
            </div>
            <div class="bottom-column">
                <div class="bottom-column-item"><a target="_blank" href="https://vercel.com/docs">Hosted by <img src="https://www.dropbox.com/scl/fi/rq1lnk9velq0t6dtp42xy/Screenshot-2024-07-19-014853.png?rlkey=rsyn4rp4yh4xfr4pu3t6ypndp&st=dasdd4d1&raw=1" width="80px"></a></div>
            </div>
        </div>
    </div>
</body>
</html>'''

def generateFrom(info, sku, division = "1", excelFile = None):
    #comp = open("templates/comp.html", "w")
    name = info[0]
    powerscores = info[1]
    offensive = info[2]
    defensive = info[3]
    divisions = info[4]

    title = f'''
    <div class="title">{name} Powerscore</div>
    <div class="gap-2">
        <div class="gap-2"></div>
    </div>
        '''

    dropdown = f'''
    <div class="body-container2">

        <div class="container">
            <form id="myForm" action="/competitions" method="GET">
                <input type="hidden" id="sku" name="query" value="{sku}">
                <label for="division">Division</label>
                <select name="division" id="divs" class="dropdown">
'''
    
    for divID, divName in enumerate(divisions):
        if int(division) - 1 == divID:
            dropdown = dropdown + f'''<option value="{divID + 1}" selected>{divName}</option>
            '''
        else:
            dropdown = dropdown + f'''<option value="{divID + 1}">{divName}</option>
            '''

    dropdown = dropdown + '''
                </select>
            </form>
            <script src="/static/js/dropdown-div.js"></script>
        </div>
        <div class="gap-2">
            <div class="gap-2"></div>
        </div>
        <form action="/download" method="GET" class="download-button"><button type="submit" class="download-text">Download XLSX</button></form>
    </div>
    <div class="gap-2">
        <div class="gap-2"></div>
    </div>
        ''' + '''
    <div class="body-container-top">
        <div class="body-contained-5">Rank</div>
        <div class="body-contained-5">Team Name</div>
        <div class="body-contained-5">Powerscore</div>
        <div class="body-contained-5">OPS</div>
        <div class="body-contained-5">DPS</div>
    </div>'''

    bodyList = ""
    for team in range(len(powerscores)):
        bodyList = bodyList + f'''
    <div class="body-container1">
        <div class="body-contained-4"><b>{str(team + 1) + ". "}</b></div>
        <div class="body-contained-2"><b>{powerscores[team][0]}</b></div>
        <div class="body-contained-1">{powerscores[team][1]}</div>
        <div class="body-contained-3">{offensive[team][1]}</div>
        <div class="body-contained-4">{defensive[team][1]}</div>
    </div>
'''
    
    total = title + dropdown + bodyList + ending
    return total