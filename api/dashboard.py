ending = '''
            <div class="big-gap">
                <div class="big-gap"></div>
            </div>
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

def generateFrom(list):
    data = ''''''
    for item in list:
        name = item['name']
        date = item['date']
        score = item['score']
        sku = item['sku']

        data = data + f'''
            <div class="dashboard" visual="tint">
                <div class="dashboard-left">
                    <div class="dashboard-left-text-title">{name}</div>
                    <div class="dashboard-left-text-body">{date}</div>
                    <form action="/competitions" method="GET">                 
                        <button class="dashboard-left-link"><u>Show Competition</u></button>
                        <input type="hidden" name="query" value="{sku}">
                        <input type="hidden" name="division" value="1">
                    </form>
                </div>
                <div class="dashboard-right">
                    <div class="dashboard-right-text-title">{score}</div>
                </div>
            </div>
            <div class="gap-2">
                <div class="gap-2"></div>
            </div>
        '''
        
    return data + ending
