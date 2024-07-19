ending = '''
        <div class="gap">
            <div class="gap"></div>
        </div>
                <div class="gap">
            <div class="gap"></div>
        </div>
                <div class="big-gap">
            <div class="big-gap"></div>
        </div>
        <div class="big-gap">
            <div class="big-gap"></div>
        </div>
        <div class="big-gap">
            <div class="big-gap"></div>
        </div>
        <div class="big-gap">
            <div class="big-gap"></div>
        </div>
        <div class="big-gap">
            <div class="big-gap"></div>
        </div>
        <div class="big-gap">
            <div class="big-gap"></div>
        </div>
        <div class="bottom">
            © Copyright 2024 by Ajaya Ramachandran, Team 8568A 23-24
            <div class="bottom-bottom">
                <div class="v-gap">
                    <div class="v-gap"></div>
                </div>
                <div class="v-gap">
                    <div class="v-gap"></div>
                </div>
                <div class="bottom-column">
                    <div class="bottom-column-item"><a target="_blank" href="https://forms.gle/uv3X3gEELeUg8D2L6">Improve This Site</a></div>
                    <div class="bottom-column-item"><a target="_blank" href="mailto:na8568a@gmail.com">Contact Us</a></div>
                    <div class="bottom-column-item"><a target="_blank" href="https://github.com/AjayaRamachandran">Support Me on GitHub</a></div>
                    <div class="bottom-column-item"><a target="_blank" href="https://www.dropbox.com/scl/fi/kug4ka2zejyvz9yduh5i3/Credits-and-Acknowledgements.pdf?rlkey=gn6tuqgpfump219muz10rduri&st=amh43ydv&dl=0">Credits</a></div>
                </div>
                <div class="bigger-gap">
                    <div class="bigger-gap"></div>
                </div>
                <div class="bigger-gap">
                    <div class="bigger-gap"></div>
                </div>
                <div class="bigger-gap">
                    <div class="bigger-gap"></div>
                </div>
                <div class="bigger-gap">
                    <div class="bigger-gap"></div>
                </div>
                <div class="bigger-gap">
                    <div class="bigger-gap"></div>
                </div>
                <div class="bigger-gap">
                    <div class="bigger-gap"></div>
                </div>
                <div class="bottom-column">
                    <div class="bottom-column-item"><a href="https://vercel.com/docs">Hosted by Vercel</div>
                </div>
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
        <div class="dashboard">
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
        <div class="gap-2"><div class="gap-2"></div></div>
'''
        
    return data + ending
