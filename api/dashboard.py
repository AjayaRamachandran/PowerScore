ending = '''
        <div class="gap">
            <div class="gap"></div>
        </div>
                <div class="gap">
            <div class="gap"></div>
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
