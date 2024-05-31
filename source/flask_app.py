from flask import Flask, request, make_response
from tempfile import NamedTemporaryFile
import transition_grid
import transitions_to_gsheets_via_pandas
from complete_the_siteswap import valid_so_far
from local_siteswaps import is_valid_local
import new_comments_gsheet

app = Flask(__name__)
app.config["DEBUG"] = True

@app.route("/")
def home_page():
    return render_template("child_home.html", image_source='/static/images/NOSPACEJUGGLEHACKER.png')


@app.route("/resources")
def resources_page():
    return render_template("child_resources.html", image_source='/static/images/NOSPACEJUGGLEHACKER.png')

@app.route("/contact", methods=["GET", "POST"])
def contact_page():
    if request.method == "GET":
        return render_template("child_contact.html",image_source='/static/images/NOSPACEJUGGLEHACKER.png')
    elif request.method == "POST":
        name = request.form["name"]
        email_address = request.form["email"]
        comment = request.form["comment"]
        new_comments_gsheet.make_new_comment(name, email_address, comment)
        return render_template("child_contact_submitted.html", image_source='/static/images/NOSPACEJUGGLEHACKER.png')


@app.route("/faqs")
def faq_page():
    return render_template("child_faqs.html", image_source='/static/images/NOSPACEJUGGLEHACKER.png')

@app.route("/gallery")
def gallery_page():
    return render_template("child_gallery.html", image_source='/static/images/NOSPACEJUGGLEHACKER.png')

@app.route("/video_gallery")
def video_gallery_page():
    return render_template("child_videos.html", image_source='/static/images/NOSPACEJUGGLEHACKER.png')

@app.route('/my-thoughts-on-hijacks')
def show_my_pdf():
    return render_template("child_my_thoughts.html", image_source='/static/images/NOSPACEJUGGLEHACKER.png')


@app.route("/hijack-generator", methods=["GET","POST"])
def testing_page():
    if request.method == "GET":
        return render_template("child_hijack_generator.html",errors='',
        starting_pattern='7,7,8,6,2',permitted_throws='2,6,7,8',email_address='optional',
        permitted_throws_flag = '', starting_pattern_flag = '')
    elif request.method == "POST":
        raw_starting_pattern = request.form["starting_pattern"]
        raw_permitted_throws = request.form["permitted_throws"]
        email_address = request.form["email_address"]
        starting_pattern_flag = '*!*  '
        permitted_throws_flag = '*!*  '
        errors = ''

        try:
            starting_pattern = [int(i) for i in raw_starting_pattern.split(',')]
            if valid_so_far(starting_pattern):
                starting_pattern_flag = ''
            else:
                errors += "{} is not a valid global siteswap.\n".format(raw_starting_pattern)
                test_if_valid_local = is_valid_local(starting_pattern) # index zero is true or false, index one has global
                if test_if_valid_local[0]:
                    valid_local_as_string = ''
                    for throw in test_if_valid_local[1]:
                        valid_local_as_string += str(throw)+','
                    valid_local_as_string = valid_local_as_string[:-1]
                    errors += "It is, however, a valid local siteswap.\n"
                    errors += "You need to enter a global siteswap.\n"
                    errors += "The global siteswap for the local you entered is {}\n".format(valid_local_as_string)

        except:
            errors += "{} is not a list of integers, separated by commas.\n".format(raw_starting_pattern)

        try:
            permitted_throws = [int(i) for i in raw_permitted_throws.split(',')]
            permitted_throws_flag = ''
        except:

            errors += "{} is not a list of integers, separated by commas.\n".format(raw_permitted_throws)
        if starting_pattern_flag == '' and permitted_throws_flag == '':
            naughty_throws = set()
            for throw in starting_pattern:
                if throw not in permitted_throws:
                    naughty_throws.add(throw)
            if len(naughty_throws) == 0:
                pass
            else:
                permitted_throws_flag = '*!*  '
                errors += "Your starting pattern contains {} which is not in you list of permitted throws\n".format(naughty_throws)
                errors += "Please make sure all the throws in your starting pattern are in your permitted throws.\n"

        if starting_pattern_flag == '' and permitted_throws_flag == '':

            if email_address not in  ["optional",""]:
                outcome = transitions_to_gsheets_via_pandas.find_network_of_hijacks(starting_pattern, permitted_throws, email_address)
                if outcome == 'Could not share workbook at last stage':
                    errors += 'A google sheet could not be shared with {}'.format(email_address)+'\n'+'Is the email correct?'+'\n'+'If so, your domain may not support sharing google sheets.'
                    return render_template("child_hijack_generator.html",errors=errors,
                                    starting_pattern=raw_starting_pattern,permitted_throws=raw_permitted_throws,email_address=email_address,
                                    permitted_throws_flag = permitted_throws_flag, starting_pattern_flag = starting_pattern_flag)

                else: # gsheet shared successfully, outsome will be an image
                        rendered_template = render_template('gsheet_transfer.html',success=True,email=email_address,image=outcome[0],legend=outcome[1])
                        return rendered_template

            else: # they want and .xlsx file
                name_of_workbook = ("starting_pattern-" + "_".join(str(i) for i in starting_pattern) + "-permitted_throws-" + "_".join(str(i) for i in permitted_throws)+'.xlsx').replace(' ','')
                wb = transition_grid.find_network_of_hijacks(starting_pattern, permitted_throws, write_to_workbook=True, workbook_name=name_of_workbook)
                wb = transition_grid.draw_network_of_hijacks(starting_pattern, permitted_throws)

                with NamedTemporaryFile() as tmp:
                    wb.save(tmp.name)
                    tmp.seek(0)
                    stream = tmp.read()

                    response = make_response(stream)
                    content_disposition = "attachment; filename={}".format(name_of_workbook)
                    response.headers["Content-Disposition"] = content_disposition
                    return response
        else:
            return render_template("child_hijack_generator.html",errors=errors,
        starting_pattern=raw_starting_pattern,permitted_throws=raw_permitted_throws,email_address=email_address,
        permitted_throws_flag = permitted_throws_flag, starting_pattern_flag = starting_pattern_flag)





from master_gsheet_script import find_all_communities

@app.route("/superuser", methods=["GET", "POST"])
def super_user_page():
    errors = ''
    if request.method == "POST":
        period = None
        permitted_throws = None
        number_of_clubs = None
        error_count = 0
        hijack_pass = None

        try:
            period = int(request.form["period"])


        except:
            error_count += 1
            errors += "<h{0}>{1} is not an integer</h{0}>\n".format(error_count,request.form["period"])

        try:
            permitted_throws = [int(i) for i in request.form["permitted_throws"].split(',')]
        except:
            error_count += 1
            errors += "<h{0}>{1} is not a list of integers, separated by commas.</h{0}>\n".format(error_count,request.form["permitted_throws"])

        try:
            number_of_clubs = int(request.form["number_of_clubs"])

        except:
            error_count += 1
            errors += "<h{0}>{1} is not an integer</h{0}>\n".format(error_count,request.form["number_of_clubs"])

        if period is not None and request.form['hijack_pass'] == 'optional':
            if period%2 == 1:
                hijack_pass = period+2
            else:
                hijack_pass = period//2+2
            if hijack_pass%2 == 0:
                error_count += 1
                errors += "<h{0}>Passive juggler is responding with a self when they can't zip. Is that what you want?</h{0}>\n".format(error_count)
                hijack_pass = None
        else:
            try:
                hijack_pass = int(request.form["hijack_pass"])
                if hijack_pass%2 == 0:
                    error_count += 1
                    errors += "<h{0}>Passive juggler is responding with a self when they can zip. Is that what you want?</h{0}>\n".format(result)
                    hijack_pass = None
            except:
                error_count += 1
                errors += "<h{0}>{1} is not an integer</h{0}>\n".format(error_count,request.form["hijack_pass"])


        if period is not None and permitted_throws is not None and number_of_clubs is not None and hijack_pass is not None:
            try:
                result = find_all_communities(period,permitted_throws,number_of_clubs,request.form["email_address"],hijack_pass)
                if result == 'No communities found!':
                    error_count += 1
                    errors += "<h{0}>No communities of hijacks were found, try different inputs</h{0}>\n".format(error_count)
                else:
                    error_count += 1
                    errors += "<h{0}>A worksheet was created, and shared with {1}.</h{0}>\n".format(error_count,request.form['email_address'])
            except:
                error_count += 1
                errors += "<h{0}>A worksheet could not be shared with {1}. Is the email correct?</h{0}>\n".format(error_count,request.form['email_address'])

    return '''
        <html>
            <head>
                <title>Juggle Hacker</title>
                <link rel="stylesheet" link href="/static/css/main.css">
                <link rel="shortcut icon" href="/static/images/beer-outline.svg">
                <img src='/static/images/NOSPACEJUGGLEHACKER.png' class="center" style="width:820px;height:460px;border:0;">
            </head>

            <body>
                <header>
                    {errors}
                </header>
                <p class="center">Enter your period, permitted throws which the patterns we transition into can contain and the number of clubs:</p>
                <form method="post" action="/superuser">
                    <p class="center"><b>Period:</b> <input name="period"/> Note: Global or local period is fine.</p>
                    <p class="center"><b>Permitted throws:</b> <input name="permitted_throws"/> Note: Enter integers with commas in between, for example 2,6,7,8 for patterns made up of zips, selfs, single passes and heffs. </p>
                    <p class="center"><b>Number of clubs:</b> <input name="number_of_clubs"/> Note: These patterns could in theory be done with other objects, I suppose. </p>
                    <p class="center"><b>Hijack pass:</b> <input name="hijack_pass" value='optional'/> Note: The passive responder will throw this if they can't zip. The active juggler will throw this at zips. If left blank defaults to local period + 2 </p>
                    <p class="center"><b>Email to send gsheet to:</b> <input name="email_address"/></p>
                    <p class="center"><input type="submit" value="Send me a google sheet"/></p>
                </form>
            </body>
        </html>
    '''.format(errors=errors)


@app.route("/old-hijack-generator", methods=["GET", "POST"])
def hijack_generator_page():
    errors = ""
    if request.method == "POST":
        starting_pattern = None
        permitted_throws = None
        valid_starting_pattern = False
        valid_permitted_throws = False
        error_count = 0
        try:
            starting_pattern = [int(i) for i in request.form["starting_pattern"].split(',')]
            if valid_so_far(starting_pattern):
                valid_starting_pattern = True
            else:
                error_count += 1
                errors += "<h{0}>{1} is not a valid global siteswap.</h{0}>\n".format(error_count,request.form["starting_pattern"])
                test_if_valid_local = is_valid_local(starting_pattern) # index zero is true or false, index one has global
                if test_if_valid_local[0]:
                    valid_local_as_string = ''
                    for throw in test_if_valid_local[1]:
                        valid_local_as_string += str(throw)+','
                    valid_local_as_string = valid_local_as_string[:-1]
                    errors += "<h{0}>It is, however, a valid local siteswap.</h{0}>\n".format(error_count)
                    errors += "<h{0}>You need to enter a global siteswap.</h{0}>\n".format(error_count)
                    errors += "<h{0}>The global siteswap for the local you entered is {1}</h{0}>\n".format(error_count,valid_local_as_string)

        except:
            error_count += 1
            errors += "<h{0}>{1} is not a list of integers, separated by commas.</h{0}>\n".format(error_count,request.form["starting_pattern"])

        try:
            permitted_throws = [int(i) for i in request.form["permitted_throws"].split(',')]
        except:
            error_count += 1
            errors += "<h{0}>{1} is not a list of integers, separated by commas.</h{0}>\n".format(error_count,request.form["permitted_throws"])
        if starting_pattern is not None and permitted_throws is not None:
            naughty_throws = set()
            for throw in starting_pattern:
                if throw not in permitted_throws:
                    naughty_throws.add(throw)
            if len(naughty_throws) == 0:
                valid_permitted_throws = True
            else:
                error_count += 1
                errors += "<h{0}>Your starting pattern contains {1} which is not in you list of permitted throws</h{0}>\n".format(error_count,naughty_throws)
                errors += "<h{0}>Please make sure all the throws in your starting pattern are in your permitted throws.</h{0}>\n".format(error_count,naughty_throws)

        if valid_starting_pattern and valid_permitted_throws:
            email_address = request.form["email_address"]
            if email_address != "optional":
                outcome = transitions_to_gsheets_via_pandas.find_network_of_hijacks(starting_pattern, permitted_throws, email_address)
                if outcome == 'Could not share workbook at last stage':
                    return render_template('gsheet_transfer.html',success=False,email=email_address)

                else: # workbooked shared successfully, outcome contains an image
                    return render_template('gsheet_transfer.html',success=True,email=email_address,image=outcome)
            else: # they want and .xlsx file
                name_of_workbook = ("starting_pattern-" + "_".join(str(i) for i in starting_pattern) + "-permitted_throws-" + "_".join(str(i) for i in permitted_throws)+'.xlsx').replace(' ','')
                wb = transition_grid.find_network_of_hijacks(starting_pattern, permitted_throws, write_to_workbook=True, workbook_name=name_of_workbook)
                wb = transition_grid.draw_network_of_hijacks(starting_pattern, permitted_throws)

                with NamedTemporaryFile() as tmp:
                    wb.save(tmp.name)
                    tmp.seek(0)
                    stream = tmp.read()

                    response = make_response(stream)
                    content_disposition = "attachment; filename={}".format(name_of_workbook)
                    response.headers["Content-Disposition"] = content_disposition
                    return response




    return '''
        <html>
            <head>
                <title>Juggle Hacker</title>
                <link rel="stylesheet" link href="/static/css/main.css">
                <link rel="shortcut icon" href="/static/images/New Favicon.png">
                <img src='/static/images/GAP at top Hijack Generator.png' class="center" style="width:820px;height:460px;border:0;">
                <a href="/hijack-generator" class="center"><img src='/static/images/Juggle Hacker Menu Icon.png' align="left" style="width:147px;height:49px;border:0;"></a>
                <a href="/faqs" class="center"><img src='/static/images/FAQ Menu Icon.png' align="left" style="width:147px;height:49px;border:0;"></a>
                <a href="/video_gallery" class="center"><img src='/static/images/Videos Menu Icon.png' align="left" style="width:147px;height:49px;border:0;"></a>
                <a href="/gallery" class="center"><img src='/static/images/Gallery Menu Icon.png' align="left" style="width:147px;height:49px;border:0;"></a>
                <a href="/contact" class="center"><img src='/static/images/Contact Menu Icon.png' align="left" style="width:147px;height:49px;border:0;"></a><br><br><br>
            </head>
            <br><br><br>
            <body>
                <h2 class="center"><center>Welcome to the Hijack Generator</center></h2>
                <header>
                    {errors}
                </header>

                <p class="center">In order to generate hijacks some information is required:</p>
                <p class="center">
                    <img src='/static/images/New Favicon.png' align="left" style="width:13px;height:13px;border:0;">
                    &nbsp;&nbsp;What pattern the two pasers are currently juggling<br>
                    <img src='/static/images/New Favicon.png' align="left" style="width:13px;height:13px;border:0;">
                    &nbsp;&nbsp;What throws the two passers can do<br>
                    <span style="font-size:small;">(For example, can they throw and catch double passes?)</span>
                </p>

                <p class="center">Please specify these by entering lists of whole numbers, separated by commas.</p>
                <p class="center">For more details on what to put in the boxes, look at the <a href="/faqs#Question8">frequently asked questions.</a></p>
                <form method="post" action="/hijack-generator">
                    <p class="center"><b>Starting pattern:</b> <input name="starting_pattern" value="7,7,8,6,2" />E.g. 7,7,8,6,2 for 6 club why not.</p>
                    <p class="center"><b>Permitted throws:</b> <input name="permitted_throws" value="2,6,7,8"/> E.g. 2,6,7,8 for patterns made up of zips, selfs, single passes and heffs. </p>
                    <p class="center">You can have your output as a spreadsheet (.xlsx file) or as a google sheet. If you want a google sheet, you need to tell me your email.</p>
                    <p class="center">Currently you only get a cool network diagram, like you can see in the <a href="/gallery">gallery</a>, if you choose a spreadsheet, but I'm working on that.</p>
                    <p class="center">If you are wondering how to read your output, have a look at the <a href="/faqs#Questionz">frequently asked questions.</a></p>
                    <p class="center"><input type="submit" value="Give me a spreadsheet of transitions" /></p>
                    <p class="center"><b>Email:</b> <input name="email_address" value="optional"/> please leave this field alone if you don't want a google sheet!</p>
                    <p class="center"><input type="submit" value="Send me a google sheet" /></p>
                </form>
            <div id="footer" class="center">
                <br>
                Juggle Hacker - A website made by Cameron Ford.
                Powered by Python <ion-icon name="logo-python"></ion-icon><ion-icon name="logo-python-outline"><ion-icon name="logo-python-sharp"></ion-icon></ion-icon>
                </div>
            <script src="https://unpkg.com/ionicons@5.0.0/dist/ionicons.js"></script>
            </body>
        </html>
    '''.format(errors=errors)

from flask import render_template
import matplotlib.pyplot as plt
from io import BytesIO
import base64
import numpy as np

def rendering_function():
    return render_template("child_faqs.html")

@app.route("/topsecret")
def top_secret_page():
    return rendering_function()

@app.route("/secret", methods = ["GET","POST"])
def secret_page():
    if request.method == "GET":
        return """
        <html>
            <body>
                <form method="post" action="/secret">
                    <p class="center"><b>x_max:</b> <input name="x_max"/></p>
                </form>
            </body>
        </html>
        """
    if request.method == "POST":
        x_max = int(request.form["x_max"])
        ### Generating X,Y coordinaltes to be used in plot
        X = np.linspace(0,x_max,3*x_max)
        Y = X*X
        ### Generating The Plot
        plt.plot(X,Y)
        # ### Saving plot to disk in png format
        # plt.savefig('/home/CameronFord/mysite/plots/square_plot{}.png'.format(x_max))

        ### Rendering Plot in Html
        figfile = BytesIO()
        plt.savefig(figfile, format='png')
        figfile.seek(0)
        figdata_png = base64.b64encode(figfile.getvalue()).decode('ascii')
        plt.close()
        return render_template('secret_template.html', image=figdata_png)

# import io
# import random
# from flask import Flask, Response, request
# from matplotlib.backends.backend_agg import FigureCanvasAgg
# from matplotlib.backends.backend_svg import FigureCanvasSVG
# import networkx as nx
# import matplotlib.pyplot as plt
# import numpy as np
# # For color mapping
# import matplotlib.colors as colors
# import matplotlib.cm as cmx
# import openpyxl
# from tempfile import NamedTemporaryFile
# import programming
# from transition_grid import siteswap_in_list

# from matplotlib.figure import Figure

# @app.route("/matplot-as-image-<string:starting_pattern>-<string:permitted_throws>.png")
# def plot_png(starting_pattern, permitted_throws):
#     """ renders the plot on the fly.
#     """
#     starting_pattern = [int(i) for i in starting_pattern]
#     permitted_throws = [int(i) for i in permitted_throws]

#     transitions_found = 0
#     patterns_found = 1
#     patterns = [starting_pattern] # keep track of all patterns found
#     new_patterns = [starting_pattern] # keep track of patterns found on latest loop
#     keep_looping = True
#     G=nx.Graph()
#     G.add_node(str(patterns_found))

#     while keep_looping:
#         newer_patterns = []
#         for pattern in new_patterns:
#             hijack = programming.generate_hijacks(pattern, permitted_throws,None,None)
#             hijack +=  programming.generate_hijacks(pattern[1:]+pattern[:1], permitted_throws,None,None)
#             for transition in hijack:

#                 if transition == None:
#                     continue
#                 transitions_found += 1
#                 index_of_pattern = siteswap_in_list(patterns, transition[1]) # None if not there

#                 if index_of_pattern == None:
#                     newer_patterns.append(transition[1])
#                     patterns.append(transition[1])
#                     patterns_found += 1
#                     G.add_node(str(patterns_found))
#                 G.add_edge(str(siteswap_in_list(patterns,transition[0])+1),str(siteswap_in_list(patterns,transition[1])+1))

#         if newer_patterns == []:
#             keep_looping = False
#         else:
#             new_patterns = newer_patterns

#     pos=nx.spring_layout(G)
#     val_map = {str(i):i for i in range(1,len(patterns)+1)}
#     ColorLegend = {str(i+1)+': '+str(patterns[i][::2])+' vs '+str(patterns[i][1::2]):(i+1) for i in range(len(patterns))}
#     values = [val_map.get(node, 0) for node in G.nodes()]
#     # Color mapping
#     jet = cm = plt.get_cmap('jet')
#     cNorm  = colors.Normalize(vmin=0, vmax=max(values))
#     scalarMap = cmx.ScalarMappable(norm=cNorm, cmap=jet)

#     # Using a figure to use it as a parameter when calling nx.draw_networkx
#     f = plt.figure(1)
#     ax = f.add_subplot(1,1,1)
#     for label in ColorLegend:
#         ax.plot([0],[0],color=scalarMap.to_rgba(ColorLegend[label]),label=label)

#     # Just fixed the color map
#     nx.draw_networkx(G,pos, cmap = jet, vmin=0, vmax= max(values),node_color=values,with_labels=True,ax=ax)

#     # Setting it to how it was looking before.
#     plt.axis('off')
#     f.set_facecolor('w')

#     #plt.legend()

#     f.tight_layout()

#     output = io.BytesIO()
#     FigureCanvasAgg(f).print_png(output)
#     return Response(output.getvalue(), mimetype="image/png")





# @app.route("/testing")
# def index():
#     """ Returns html with the img tag for your plot.
#     """
#     num_x_points = int(request.args.get("num_x_points", 50))
#     # in a real app you probably want to use a flask template.
#     return """
#     <h1>Flask and matplotlib</h1>
#     <h2>Random data with num_x_points={0}</h2>
#     <form method=get action="/">
#       <input name="num_x_points" type=number value="{0}" />
#       <input type=submit value="update graph">
#     </form>
#     <h3>Plot as a png</h3>
#     <img src="/matplot-as-image-{0}.png"
#          alt="random points as png"
#          height="200"
#     >
#     """.format(num_x_points)
#     # from flask import render_template
#     # return render_template("yourtemplate.html", num_x_points=num_x_points)


# @app.route("/matplot-as-image-<int:num_x_points>.png")
# def plot_png(num_x_points=50):
#     """ renders the plot on the fly.
#     """
#     fig = Figure()
#     axis = fig.add_subplot(1, 1, 1)
#     x_points = range(num_x_points)
#     axis.plot(x_points, [random.randint(1, 30) for x in x_points])

#     output = io.BytesIO()
#     FigureCanvasAgg(fig).print_png(output)
#     return Response(output.getvalue(), mimetype="image/png")
