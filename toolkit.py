import PySimpleGUI as sg
import requests
import webbrowser
import subprocess
import platform
from faker import Faker

fake = Faker()

# Text font + size
main_f = ('Comic Sans MS', 15)
main_fs = ('Comic Sans MS', 12)

# PySimpleGUI theme
sg.theme('DarkBlue17')

# Creates the main window layout with some basic device info
mainWindowlayout = [[sg.Text('My Toolkit', font=('Comic Sans MS', 20))],
                    [sg.Text('Device Name: ' + platform.node(), font=main_fs)],
                    [sg.Text('Operating System: ' + platform.system() + ' ' + platform.release(), font=main_fs)],
                    [sg.Text('Version: ' + platform.version(), font=main_fs)],
                    [sg.Text('Python Version: ' + platform.python_version(), font=main_fs)],
                    [sg.Button('IP Scanner', font=main_fs), sg.Button('Email Checker', font=main_fs), sg.Button('System Info', font=main_fs)],
                    [sg.Button('Fake Info Generator', font=main_fs), sg.Button('Placeholder2', font=main_fs), sg.Button('Placeholder3', font=main_fs)],
                    [sg.Exit(font=main_fs)]]

MainWindow = sg.Window('My toolkit', icon=r'icon.ico', grab_anywhere=True).Layout(mainWindowlayout)


# Function that creates the main window when called
def main_window():
    layout = [[sg.Text('My Toolkit', font=('Comic Sans MS', 20))],
                    [sg.Text('Device Name: ' + platform.node(), font=main_fs)],
                    [sg.Text('Operating System: ' + platform.system() + ' ' + platform.release(), font=main_fs)],
                    [sg.Text('Version: ' + platform.version(), font=main_fs)],
                    [sg.Text('Python Version: ' + platform.python_version(), font=main_fs)],
                    [sg.Button('IP Scanner', font=main_fs), sg.Button('Email Checker', font=main_fs), sg.Button('System Info', font=main_fs)],
                    [sg.Button('Fake Info Generator', font=main_fs), sg.Button('Placeholder2', font=main_fs), sg.Button('Placeholder3', font=main_fs)],
                    [sg.Exit(font=main_fs)]]
    return sg.Window('My Toolkit', layout, icon=r'icon.ico', grab_anywhere=True)


while True:

    event, values = MainWindow.Read()

    if event in (None, 'Exit'):
        MainWindow.close()
        break

    elif event == 'IP Scanner':
        MainWindow.close()

        ipscannerLayout = [[sg.Text('Enter the ip address you would like to scan: ', font=main_f)], [sg.InputText()], [sg.Button('Submit', font=main_fs), sg.Exit(font=main_fs)]]

        IPscannerwindow = sg.Window('IP Scanner', ipscannerLayout, icon=r'icon.ico', grab_anywhere=True)
        event, values2 = IPscannerwindow.Read()

        keepRunning = True

        while keepRunning is True:

            if event in (None, 'Exit'):
                IPscannerwindow.close()
                MainWindow = main_window()
                break

            if event == "Submit":

                text_input = values2[0]
                results = requests.get("https://internetdb.shodan.io/" + str(text_input)).json()

                # Sorts the vulnerabilities by year from oldest to newest
                results["vulns"].sort()

                # If statement checks to see if the amount of vulns detected is greater than 0
                # If it is, a listbox listing the results is created, otherwise no listbox is created and the user is notified
                if len(results["vulns"]) > 0:

                    layoutIPscanresults = [[sg.Text("IP Scanned: ")], [sg.Text(text_input)], [sg.Text("Open ports:")],
                                           [sg.Text(results['ports'])],
                                           [sg.Text("Vulnerabilities:")],
                                           [sg.Listbox(results["vulns"], size=(50, len(results["vulns"])), key='-VULN-',
                                                       enable_events=True, text_color='blue')],
                                           [sg.Button('Exit', key='Exit', size=(10, 1))]]
                else:
                    layoutIPscanresults = [[sg.Text("IP Scanned: ")], [sg.Text(text_input)], [sg.Text("Open ports:")],
                                           [sg.Text(results['ports'])],
                                           [sg.Text("No vulnerabilities detected.")],
                                           [sg.Button('Exit', key='Exit', size=(10, 1))]]

                IPresultswindow = sg.Window("IP Results", layoutIPscanresults, icon=r'icon.ico', grab_anywhere=True)

                url_opened = None

                while True:
                    event, IPvalues = IPresultswindow.Read()
                    if event == sg.WIN_CLOSED or event == "Exit":
                        IPresultswindow.Close()
                        break
                    if event == "-VULN-":
                        selected_url = IPvalues["-VULN-"][0]
                        selected_index = results["vulns"].index(selected_url)
                        if selected_url != url_opened:
                            url_opened = selected_url
                            webbrowser.open("https://nvd.nist.gov/vuln/detail/" + selected_url)

                IPscannerwindow.Close()
                MainWindow = main_window()
                keepRunning = False



    elif event == 'Email Checker':

        MainWindow.close()

        emailcheckerLayout = [[sg.Text('Scan for compromised passwords leaked in data breaches.', font=main_fs)],
                              [sg.Text('Allows you to target a specific email address.', font=main_fs)],
                              [sg.Text('Please enter the email address you wish to check: ', font=main_fs)],
                              [sg.InputText()],
                              [sg.Button('Submit', font=main_fs), sg.Exit(font=main_fs)]]

        EmailCheckerWindow = sg.Window('Email Checker', emailcheckerLayout, icon=r'icon.ico', grab_anywhere=True)

        event, values3 = EmailCheckerWindow.Read()

        keepRunning = True

        while keepRunning is True:

            if event in (None, 'Exit'):
                EmailCheckerWindow.close()
                MainWindow = main_window()
                break

            if event == "Submit":
                text_input = values3[0]
                url = "https://breachdirectory.p.rapidapi.com/"
                querystring = {"func": "auto", "term": "{}".format(text_input)}
                headers = {

                    "X-RapidAPI-Key": "YOUR-BREACH-DIRECTORY-API-HERE",  # <==================CHANGE TO YOUR OWN API

                    "X-RapidAPI-Host": "breachdirectory.p.rapidapi.com"

                }

                response = requests.request("GET", url, headers=headers, params=querystring).text

                sg.popup_scrolled('Results', response, icon=r'icon.ico', grab_anywhere=True)

                EmailCheckerWindow.close()
                MainWindow = main_window()

                keepRunning = False




    elif event == 'System Info':

        MainWindow.close()

        sysinfoLayout = [[sg.Text('Use this tool to gather system information', font=main_f)],

                         [sg.Text('Operating System, Architecture, IP addressing, Hotfixes, Network Cards, DHCP, etc..', font=main_fs)],

                         [sg.Button('Gather', font=main_fs), sg.Exit(font=main_fs)],
                         [sg.Output(size=(65, 20), font=('Helvetica', 18), key='sysinfo')]]

        systeminfowindow = sg.Window('System Info', sysinfoLayout, icon=r'icon.ico', grab_anywhere=True)

        keepRunning = True

        while keepRunning is True:

            event, values4 = systeminfowindow.Read()

            if event in (None, 'Exit'):
                systeminfowindow.close()

                MainWindow = main_window()

                keepRunning = False

                break

            if event in (None, 'Gather'):

                Id = subprocess.check_output(['systeminfo']).decode('utf-8').split('\n')

                new = []

                # arrange the string into clear info

                for item in Id:
                    new.append(str(item.split("\r")[:-1]))

                formatted_list = [i[2:-2] for i in new]

                print('\n'.join(formatted_list))



    elif event == 'Fake Info Generator':
        MainWindow.close()

        fakeinfoLayout = [
            [sg.Text('Select the information you want to generate:', font=main_f)],
            [sg.Checkbox('Name', default=False, key='name', font=main_fs), sg.Checkbox('License Plate', default=False, key='license_plate', font=main_fs), sg.Checkbox('Email', default=False, key='email', font=main_fs)],
            [sg.Checkbox('Address', default=False, key='address', font=main_fs), sg.Checkbox('Credit Card', default=False, key='credit_card', font=main_fs), sg.Checkbox('Job title', default=False, key='job_title', font=main_fs)],
            [sg.Checkbox('Phone Number', default=False, key='phone', font=main_fs), sg.Checkbox('Ipv4 addr.', default=False, key='ipv4_addr', font=main_fs), sg.Checkbox('Ipv6 addr.', default=False, key='ipv6_addr', font=main_fs)],
            [sg.Checkbox('Social Security Number', default=False, key='ssn', font=main_fs), sg.Checkbox('Mac Addr.', default=False, key='mac_addr', font=main_fs), sg.Checkbox('Coordinates', default=False, key='latlng', font=main_fs)],
            [sg.Button('Generate', font=main_fs), sg.Button('Exit', font=main_fs), sg.Button('Select/Deselect ALL', font=main_fs)],
            [sg.Output(size=(65, 20), font=('Helvetica', 18), key='generatedinfo')]
        ]


        fakeinfoWindow = sg.Window('Fake Information Generator', fakeinfoLayout, grab_anywhere=False, icon=r'icon.ico')

        keepRunning = True

        checkbox_states = {key: True if key == 'test' else False for key in ['name', 'address', 'phone', 'ssn', 'job_title', 'email', 'license_plate', 'credit_card', 'ipv4_addr', 'ipv6_addr', 'mac_addr', 'latlng']}
        check_all_state = False

        while keepRunning is True:
            event, values = fakeinfoWindow.read()
            if event == sg.WINDOW_CLOSED or event == 'Exit':
                break

            if event == 'Generate':

                # User selects the info they want generated
                generated_info = ''
                if values['name']:
                    generated_info += "Name: " + fake.name() + '\n'
                if values['address']:
                    generated_info += "Address: " + fake.address() + '\n'
                if values['phone']:
                    generated_info += "Phone Number: " + fake.phone_number() + '\n'
                if values['job_title']:
                    generated_info += "Job Title: " + fake.job() + '\n'
                if values['ssn']:
                    generated_info += "SSN: " + fake.ssn() + '\n'
                if values['email']:
                    generated_info += "Email: " + fake.ascii_email() + '\n' + '\n'
                if values['license_plate']:
                    generated_info += "License Plate: " + fake.license_plate() + '\n'
                if values['credit_card']:
                    generated_info += "Credit Card: " + fake.credit_card_full() + '\n'
                if values['ipv4_addr']:
                    generated_info += "Ipv4 Address: " + fake.ipv4() + '\n'
                if values['ipv6_addr']:
                    generated_info += "Ipv6 Address: " + fake.ipv6() + '\n'
                if values['mac_addr']:
                    generated_info += "Mac Address: " + fake.mac_address() + '\n'
                if values['latlng']:
                    lat, lng = fake.latlng()
                    generated_info += "Coordinates: ({}, {})\n".format(lat,lng)


                # outputs generated info to the window
                fakeinfoWindow['generatedinfo'].update(generated_info)

            if event == 'Select/Deselect ALL':
                # Set the value of all checkboxes to True
                check_all_state = not check_all_state
                for key in checkbox_states.keys():
                    checkbox_states[key] = check_all_state
                    fakeinfoWindow[key].update(checkbox_states[key])




        # Closes the fake info generator and re-opens main window
        fakeinfoWindow.close()
        MainWindow = main_window()


    #elif event == 'Placeholder2':
        #stuff
