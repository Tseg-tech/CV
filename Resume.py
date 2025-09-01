from fpdf import FPDF

from pdf2image import convert_from_path

import os
# Input/Output folders
input_dir = "input_dir"
output_dir = "images"
os.makedirs(output_dir, exist_ok=True)
# Loop over all PDF files in the folder
for filename in os.listdir(input_dir):
    if filename.endswith(".pdf"):
        pdf_path = os.path.join(input_dir, filename)
        images = convert_from_path(pdf_path, dpi=200)

    for i, page in enumerate(images):
        output_file = os.path.join(output_dir, f"{filename.replace('.pdf','')}_page{i+1}.jpg")
        page.convert("RGB").save(output_file, "JPEG")
        print(f"✅ Converted: {filename} → {output_file}")
       # output_file = os.path.join(output_dir, filename.replace(".pdf", ".png"))
        #images[0].save(output_file, "PNG")

        #print(f"✅ Converted: {filename} → {output_file}")

def clean_text(text):
    # Replaces unsupported characters and keeps only ASCII-safe characters
    return text.replace("–", "-").replace("—", ".").replace("“", "\"").replace("”", "\"").replace("‘", "'").replace("’", "'")

class PDF(FPDF):
    def __init__(self):
        super().__init__()
        self.show_header = True  # Show header by default

    def header(self):

        # Shared part: shown on all pages
            # Set font and alignment
        pdf.add_font("DejaVu", "", "DejaVuSans.ttf", uni=True)
        pdf.set_font("DejaVu", "", 12)


        # ───── Segment 1: Job Title ─────
        self.set_text_color(0, 0, 0)
        self.cell(60, 10, "Full-Stack Developer", border=0, ln=0, align="C")

        # Separator
        self.set_text_color(0, 0, 0)
        self.cell(10, 10, "|", border=0, ln=0, align="C")

# ───── Segment 2: LinkedIn Link ─────
        self.set_text_color(0, 0, 255)
        self.cell(60, 10, "LinkedIn", border=0, ln=0, align="C", link="https://www.linkedin.com/in/tseganeh-amare/")

        # Separator
        self.set_text_color(0, 0, 0)
        self.cell(10, 10, "|", border=0, ln=0, align="C")

        # ───── Segment 3: GitHub Icon + Text (Linked Together) ─────

        # Save current X and Y
        github_x = self.get_x()
        github_y = self.get_y()

# Draw GitHub icon
        self.image("github.png", x=github_x, y=github_y + 2, w=4.5)

        # Move next to icon
        self.set_x(github_x + 6)

        # Draw GitHub text
        self.set_text_color(0, 0, 255)
        pdf.add_font("DejaVu", "", "DejaVuSans.ttf", uni=True)
        pdf.set_font("DejaVu", "", 12)

        self.cell(30, 10, "GitHub", border=0, ln=0, align="L")

        # Overlay a clickable link across icon + text
        self.link(github_x, github_y + 2, 35, 6, "https://github.com/Tseg-tech")

        # Finalize line
        self.ln(10)
        y = self.get_y()  # Current vertical position
        # First segment - Red
        self.set_draw_color(255, 153, 153)
        self.set_line_width(2)
        self.line(10, y, 70, y)

        # Second segment - Green
        self.set_draw_color(0, 204, 204)
        self.line(70, y, 130, y)

        # Third segment - Blue
        self.set_draw_color(102, 178, 0)
        self.line(130, y, 200, y)

        self.ln(5)

        self.ln(5)

    
        if self.page_no() == 1:
        # Full header on the first page
            pdf.add_font("DejaVu", "", "DejaVuSans.ttf", uni=True)
            pdf.set_font("DejaVu", "", 12)
            self.set_text_color(0, 0, 0)
            self.cell(0, 10, "Tseganeh Amare Biresaw", ln=True, align="C")
             
            pdf.add_font("DejaVu", "", "DejaVuSans.ttf", uni=True)
            pdf.set_font("DejaVu", "", 12)
            self.set_text_color(0, 0, 0)
            self.cell(0, 10, "Email: tseganehamare@gmail.com | Phone: +251 0928676954 | Addis Ababa, Ethiopia", ln=True, align="C")

            y = self.get_y()  # Current vertical position

            # First segment - Red
            self.set_draw_color(0, 0, 0)
            self.set_line_width(1)
            self.line(10, y, 70, y)

            # Second segment - Green
            self.set_draw_color(0, 0, 0)
            self.line(70, y, 130, y)

            # Third segment - Blue
            self.set_draw_color(0, 0, 0)
            self.line(130, y, 200, y)

            self.ln(5)
    
    def section_title(self, title):

        y = self.get_y()
        self.set_line_width(0.2)
        self.set_font('Arial', 'B', 12)

    # Left segment - Red
        self.set_draw_color(0, 0, 0)
        self.line(10, y + 4, 70, y + 4)

        # Title
        self.set_text_color(0, 0, 0)
        pdf.add_font("DejaVu", "", "DejaVuSans.ttf", uni=True)
        pdf.set_font("DejaVu", "", 12)
        self.set_xy(60, y)  # x = 60, y = current
        self.cell(80, 8, clean_text(title), border=0, ln=0, align="C")

        # Right segment - Blue
        self.set_draw_color(0, 0, 0)
        self.line(140, y + 4, 200, y + 4)

        # Move to next line
        self.ln(10)

    def subsection_title(self, title):
        
        self.set_font("DejaVu", "", 12)
        self.set_text_color(50, 50, 50)
        self.cell(0, 8, title, ln=True)
        self.ln(1)
    def multi_subsections(self, subsections: list):
    
        for title, body in subsections:
            self.subsection_title(title)
            self.section_body(body, bullet=True)

    def section_body(self, text, bullet=False):
        pdf.add_font("DejaVu", "", "DejaVuSans.ttf", uni=True)
        pdf.add_font("DejaVu", "B", "DejaVuSans-Bold.ttf", uni=True)  # Ensure bold font added once

        pdf.set_font("DejaVu", "", 12)
        self.set_text_color(60, 60, 60)

        lines = text.strip().split('\n')

        if bullet:
            for line in lines:
                stripped_line = line.lstrip()
                indent_level = len(line) - len(stripped_line)

                bold_labels = [
                    "Objective:", 
                    "Tools and Technologies:", 
                    "Tasks:",
                    "Languages:",
                    "Frameworks:",
                    "API Development:",
                    "Databases:",
                    "Virginia Tech, Furman University & MUST:",
                    "Cisco Networking Academy and Addis Ababa University:",
                ]
                
                bold_full_line = "Windows Server 2022 Home Lab Project: March 2024 - present"

                if indent_level == 0:
                    self.set_x(20)
                    self.cell(5, 6, "•", ln=0)  # bullet

                    # If line starts exactly with full bold line
                    if stripped_line.startswith(bold_full_line):
                        self.set_font("DejaVu", "B", 12)
                        self.multi_cell(0, 6, clean_text(stripped_line))
                        self.set_font("DejaVu", "", 12)

                    else:
                        # Otherwise, check for labels to bold only label part
                        label_found = False
                        for label in bold_labels:
                            if stripped_line.startswith(label):
                                label_found = True
                                label_len = len(label)
                                self.set_font("DejaVu", "B", 12)
                                self.cell(self.get_string_width(label), 6, label, ln=0)
                                self.set_font("DejaVu", "", 12)
                                self.multi_cell(0, 6, clean_text(stripped_line[label_len:]))
                                break

                        if not label_found:
                            self.set_font("DejaVu", "", 12)
                            self.multi_cell(0, 6, clean_text(stripped_line))


                else:
                    self.set_x(30)
                    self.set_font("DejaVu", "", 12)
                    self.multi_cell(0, 6, clean_text(stripped_line))

            self.ln(3)

        else:
            self.multi_cell(0, 6, clean_text(text))
            self.ln(3)


# Create the PDF
pdf = PDF()
pdf.add_page()

# Add this line
pdf.add_font("DejaVu", "", "DejaVuSans.ttf", uni=True)
pdf.set_font("DejaVu", "", 12)

pdf.section_title("Profile")
pdf.section_body("Full Stack Developer and Certified Drone Pilot Instructor (AUVSI) with a strong background in unmanned systems, electronics, and communication technologies. CCNA-certified across all core modules (CCNA 1, 2, and 3), with hands-on experience in building and integrating unmanned ground vehicles (UGVs) using Veronte Autopilot systems. Skilled in embedded programming, electronics design, and control systems integration. Experienced with Ultramotion servo systems, interfacing with various industrial and communication sensors, and working with advanced tactical communication solutions including DTC (Domo Tactical Communications) radios. Combines deep technical knowledge with practical field experience, offering a robust skill set ideal for autonomous systems development, drone instruction, and networked Automated solutions.")
pdf.section_title("Skills")
pdf.section_body(
    "Languages: HTML,CSS,JavaScript,c++\n"
    "Frameworks: Bootstrap,React, Node.js, Express\n"
    "API Development: RESTful APIs, JWT Authentication, OAUTH2, Postman\n"
    "Databases: MongoDB,PostgreSQL, SQLite (for testing/small projects)\n"
    "UAV/UGV Development & Integration\n"
    "Veronte Autopilot Systems\n"
    "Programming and Configuring Ultramotion Servos\n"
    "Industrial Sensor Interfacing\n"
    "DTC (Domo Tactical) Radio Systems\n"
    "Embedded Programming & Electronics\n"
    "Networking, Routing, Switching & Automation\n"
    "Soft Skills: Problem-solving, team collaboration, mentorship, software testing",
    bullet=True
   # bullet=True
)

pdf.section_title("Professional Experience")
pdf.multi_subsections ([
                        ("INSA- Trainee ","On-Site\nAddis Ababa,2017-01-30 - 2017-10-05"),
                        ("INSA- GNC Researcher ","On-Site\nAddis Ababa,2017-10-06 - 2020-06-09"),
                        ("INSA- Remote Control Software Developer ","On-Site\nAddis Ababa,2020-06-102 - 2022-04-12"),
                        ("INSA- Avionics and System Control(Remote Control Software Developer Supervisor)  ","On-Site\nAddis Ababa,2022-04-13 - up to Now"),
    
                        ("Programming Languages", "JavaScript\nC++\nBlock Programming\nPython"),
                        ("Tools & Platforms", "Git\nDocker\nLinux\nCisco Packet Tracer\n4xVerontePDIbuilder\n1xVerontePDIbuilder\nVeronte Ops\nDomo Node Finder\nQGis"
                        "\nOracle VirtualBox,Linux OS (Ubuntu)"
                        "\nVMware,Windows Server 2022, Active Directory Tools,Group Policy Management Console, Windows 10 Enterprise\nSerial Communication & Terminal Emulators(PUTTY,Tera Term)\nWireshark Network Analyzer"),
                        (
                        "Full-Stack Developer ","Built RESTful APIs using Node.js and collaborative projects.\n"
                        "Participated in agile development practices, version control with Git, and peer code reviews.\nDeveloped database schemas and implemented token-based authentication.\n"
                        )
                        ])
#pdf.section_body(
   
  #  bullet=True
#)

pdf.section_title("Projects")
pdf.multi_subsections ([
                        ("E-Commerce APP","Build, deploy, and scale an E-Commerce app using Microservices built with Node, React, Docker and Kubernetes"
                        "\nOn the frontend, i use React and Next JS to present content to users\n"
                        "Each service is created using Node and Express.Data for each service is held in a Mongo database.The entire app is deployed and runs in Docker containers executed in a Kubernetes cluster"
                        ),
                        (
                        "Autonomous UGV System",
                        "Designed and built an Unmanned Ground Vehicle (UGV) using Veronte autopilot for navigation and control.\n"
                        "Developed embedded software to interface with Ultramotion servo systems and industrial sensors.\n"
                        "Integrated DTC (Domo Tactical Communications) radio for secure telemetry and remote command."
                        ),
                        (
                        "Windows Server 2022 Home Lab Project: March 2024 - present",
                        "Objective: Set up a Windows Server environment to practice Active Directory management and network configuration.\n"
                        "Tools and Technologies: VMware, Windows Server 2022, Active Directory Tools, Group Policy Management Console, Windows 10 Enterprise\n"
                        "Tasks:\n"
                        "    - Installed and configured Windows Server 2022 on a virtual machine\n"
                        "    - Set up and managed Active Directory, including creating and managing user accounts, groups, and organizational units\n"
                        "    - Implemented Group Policy Objects (GPOs) to enforce security policies\n"
                        "    - Set up file sharing within the AD environment"
                        ),
                        (
                        "Linux in a Virtual Machine Home Lab Project",
                        "Objective: Prepare a Computer for Virtualization,Install a Linux OS on the Virtual Machine and Explore the GUI.\n"
                        "Tools and Technologies: Oracle VirtualBox , Linux OS image(ubuntu)\n"
                        "Tasks:\n"
                        "   Part 1: Prepare a Computer for Virtualization\n"
                        "    - Step 1: Download and install VirtualBox\n"
                        "    - Step 2: Download a Linux Image\n"
                        "    - Step 3: Create a New Virtual Machine\n"
                        "   Part 2: Install Ubuntu on the virtual machine\n"
                        "    - Step 1: Mount the Image\n"
                        "    - Step 2: Install the OS\n"
                        "   Part 3: Explore the GUI\n"
                        "    - Step 1: Install Guest Additions\n"
                        )

                        ]
                        )

###pdf.section_body(
    
     #bullet=True
#)

pdf.section_title("Education")
pdf.multi_subsections(
    [
    (  " Electrical Engineering",
        "Addis Ababa Institute Of Technology | Addis Ababa, Ethiopia\n"
        "10/2012 - 07/2016"
    )
    ]
)
pdf.section_title("Courses")
pdf.multi_subsections([
                        (
                            "CCNA: Introduction to Networks",
                            "Cisco Networking Academy and Addis Ababa University:\n"
                            " Skills: Ethernet,IP connectivity,IP services,IP Subnetting,IPv4 And IPv6 Addressing,Network Fundamentals,Security Fundamentals,Switching!\n"
                            "May 02, 2025 | School of Information Technology and Engineering (SITE), Addis Ababa University, Ethiopia"
                        ),
                        (
                            "CCNA: Switching, Routing, and Wireless Essentials",
                            "Cisco Networking Academy and Addis Ababa University:\n"
                            " Skills: Access Connectivity,Access Security,First-hop Redundancy,High Availability,IP services,Routing,Switching Protocols,Wireless LAN Controllers!\n"
                            "June 25, 2025 |School of Information Technology and Engineering (SITE), Addis Ababa University, Ethiopia"
                        ),
                        (
                            "CCNA: Enterprise Networking, Security, and Automation",
                            "Cisco Networking Academy and Addis Ababa University:\n"
                            " Skills: Dynamic Routing,Network Address Translation (NAT),Network Automation Basics,Quality Of Service (QoS),Security Threat Mitigation,Software Driven Networks,Virtualization,Wide Area Networks!\n"
                            "August 28, 2025 | School of Information Technology and Engineering (SITE), Addis Ababa University, Ethiopia"
                        ),
                        (
                            "Certificate of Drone and Data Technology Level 1",
                            "Virginia Tech, Furman University & MUST:\n" 
                                " 1) Data Module - The first 3 weeks cover data analysis; GIS fundamentals, data types & co-ordinate systems, multispectral sensing, introduction to computer vision and machine learning, advanced spatial analysis methods, data ethics etc. Different mapping applications e.g. agriculture, disease control, emergency response, flood modeling, infrastructure management etc.\n"
                                " 2) Drone Module - In the 4th & 5th week, students are introduced to unmanned aerial systems; flight physics, aircraft performance, propulsion systems, aerostructures, payloads, flight operations, wireless communications etc. will also be covered\n"
                            "4 Sep – 7 Oct, 2022 | Malawi University of Science and Technology(MUST),Malawi "
                        ),
                        (
                            "Certificate of Drone and Data Technology Level 2",
                            "Virginia Tech, Furman University & MUST:\n"
                            " CDDT Level 2 is a 6 week in-person course that builds on the theory covered in CDDT Level 1. Various lab sessions e.g. propulsion systems, camera integration, radios are covered.Build fixed wing and quadcopter drones from scratch, troubleshoot them, and fly them. Furthermore, work on design projects that include data collection campaigns and analysis. A hands-on entrepreneurship module is also included.\n" 
                                "  1) CDDT Level 2 Certificate issued by Virginia Tech, Furman University, and Malawi University of Science and Technology (MUST).\n"
                                "  2) Trusted Operator Program (TOP) Level 2 Certificate issued by AUVSI\n"
                                "  3) Malawi Remote Pilot License (RPL) issued by Malawi Department of Civil Aviation (DCA)\n"
                            "20 Feb – 31 March, 2022 | Malawi University of Science and Technology(MUST),Malawi "
                        ),
                        (
                            "Remote Pilot Instructor",
                            "Virginia Tech, Furman University & MUST: \n"
                            "   A) Trusted Operator Program (TOP) Instructor Certificate issued by AUVSI!\n"
                            "28 Oct - 31 Oct, 2024 | Malawi University of Science and Technology(MUST),Malawi "
                        )
                        ]
)
pdf.add_font("DejaVu", "I", "DejaVuSans-Oblique.ttf", uni=True)
pdf.section_title("Languages")
pdf.section_body("English - Professional Proficiency\nAmharic - Native")

pdf.section_title("Interests")
pdf.section_body("System Design | Studying | Continuous Learning")
pdf.add_page()

# Use write to add clickable link for the first certification

certifications = [

    ("CCNA: Introduction to Networks, 2025", "https://www.credly.com/badges/d920cb13-90c0-4f1b-b06b-8f4402dafbe2","images/Introduction to Networks.jpg"),
    
    ("CCNA: Switching, Routing, and Wireless Essentials, 2025", "https://www.credly.com/badges/9ab3b28f-6ed9-4716-a530-7519b59f60a1","images/Switching, Routing, and Wireless Essentials.jpg"),

    ("CCNA: Enterprise Networking, Security, and Automation, 2025", "https://www.credly.com/badges/6428e466-37cb-4804-80b9-d75da09b8190/public_url","images/Enterprise Networking, Security, and Automation.jpg"),

    ("Remote Pilot Instructor","https://drive.google.com/file/d/1V4Vp6x1ETl39WxECLq_UXUO-gN5BUYCv/view?usp=sharing","images/Remote Pilot Instructor.jpg"),

    ("Certificate Of Drone And Data Technology","https://drive.google.com/file/d/1hiEs1yay5KHm4rymU5A0L3Ni5PmGGwBX/view?usp=sharing","images/Certificate of Drone and Data Technology.jpg"),

    ("Build Dynamic Web Apps with React & Firebase ","https://www.udemy.com/certificate/UC-00941c02-ba77-494b-8770-35063abdb842/","images/Build Dynamic Web Apps with React & Firebase.jpg"),

    ("Build, deploy, and scale an E-Commerce app using Microservices built with Node, React, Docker and Kubernetes ","https://www.udemy.com/certificate/UC-00941c02-ba77-494b-8770-35063abdb842/","images/Introduction to Networks.png")
    ]

# Loop
first_cert = True

for cert_text, cert_link, stub in certifications:
    if first_cert:
        pdf.section_title("Certifications")  # title only on first page
        first_cert = False
    else:
        pdf.add_page()  # start a new page for all other certificates
    pdf.set_font("Arial", "I", 12)
    pdf.set_text_color(0, 0, 255)
    pdf.set_x(20)
    pdf.write(8, clean_text(cert_text), cert_link)
    pdf.ln(10)

    # Show badge if we have one
    if stub and os.path.exists(stub):
        pdf.image(stub, x=20, y=pdf.get_y(), w=180,h=180)
        pdf.ln(190)

   
pdf.set_font("DejaVu", "", 12)
pdf.set_text_color(0, 0, 0)
pdf.set_x(20)  # 


# Save PDF to file
output_path = "Tseganeh Amare Biresaw.pdf"
pdf.output(output_path)

print(f"PDF created successfully: {output_path}")




