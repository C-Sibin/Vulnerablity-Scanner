from flask import Flask, render_template, request, send_file, jsonify
import subprocess
import os
import html
from fpdf import FPDF

app = Flask(__name__)

# Function to run shell commands
def run_command(command):
    result = subprocess.run(command, shell=True, capture_output=True, text=True)
    return result.stdout

# Function to collect system information
def get_system_information():
    system_info = {}
    system_info['OS'] = run_command("systeminfo")
    system_info['.NET Framework Versions'] = run_command("reg query HKLM\\SOFTWARE\\Microsoft\\NET Framework Setup\\NDP")
    system_info['Installed Programs'] = run_command("wmic product get name,version")
    system_info['Firewall Rules'] = run_command("netsh advfirewall firewall show rule name=all")
    system_info['Hotfixes'] = run_command("wmic qfe list")
    system_info['Local Users'] = run_command("net user")
    system_info['Local Groups'] = run_command("net localgroup")
    return system_info

# Function to collect network information
def get_network_information():
    network_info = {}
    network_info['ARP Table'] = run_command("arp -a")
    network_info['DNS Cache'] = run_command("ipconfig /displaydns")
    network_info['Network Shares'] = run_command("net share")
    network_info['TCP Connections'] = run_command("netstat -an | findstr /R \"^TCP\"")
    network_info['UDP Connections'] = run_command("netstat -an | findstr /R \"^UDP\"")
    return network_info

# Function to generate PDF report
def generate_pdf_report(system_info, network_info, output_file):
    pdf = FPDF()
    pdf.add_page()
    pdf.set_font("Arial", size=12)
    
    pdf.cell(200, 10, txt="System and Network Information Report", ln=True, align="C")

    pdf.ln(10)
    pdf.set_font("Arial", size=10)
    pdf.cell(0, 10, txt="System Information:", ln=True)

    for key, value in system_info.items():
        pdf.multi_cell(0, 10, txt=f"{key}:\n{value}")

    pdf.ln(10)
    pdf.cell(0, 10, txt="Network Information:", ln=True)

    for key, value in network_info.items():
        pdf.multi_cell(0, 10, txt=f"{key}:\n{value}")

    pdf.output(output_file)

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/scan', methods=['POST'])
def run_scan():
    # Directory for storing reports
    reports_dir = 'reports'
    os.makedirs(reports_dir, exist_ok=True)
    
    output_file = os.path.join(reports_dir, 'report.pdf')
    
    # Generate system and network information
    system_info = get_system_information()
    network_info = get_network_information()

    # Generate the PDF report
    generate_pdf_report(system_info, network_info, output_file)
    
    # Return JSON result to update the webpage
    return jsonify({
        "message": "Scan completed successfully.",
        "system_info": system_info,
        "network_info": network_info,
        "download_link": "/download"
    })

@app.route('/download')
def download_report():
    return send_file('reports/report.pdf', as_attachment=True)

if __name__ == '__main__':
    app.run(debug=True)
