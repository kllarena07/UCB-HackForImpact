import os
import requests
from flask import Flask, request, jsonify
from flask_cors import CORS
import assemblyai as aai
from dotenv import load_dotenv
from openai import OpenAI, ChatCompletion
load_dotenv()

data = """
1. **Graphic Designer**
   - **Description:** Graphic designers create visual concepts, using computer software or by hand, to communicate ideas that inspire, inform, and captivate consumers. They develop the overall layout and production design for various applications such as advertisements, brochures, magazines, and corporate reports.
   - **Core Values:** Creativity, Attention to Detail, Problem-solving, Communication.
   - **Necessary Skills:** Proficiency in graphic design software (e.g., Adobe Creative Suite), typography, layout design, understanding of color theory, ability to work under pressure, communication skills.
2. **UI/UX Designer**
   - **Description:** UI/UX designers are responsible for enhancing user satisfaction by improving the usability, accessibility, and pleasure provided in the interaction between the user and the product. They create wireframes, mockups, and prototypes to design intuitive and user-friendly digital experiences.
   - **Core Values:** User-Centric Design, Empathy, Innovation, Collaboration.
   - **Necessary Skills:** Proficiency in design tools (e.g., Sketch, Adobe XD, Figma), understanding of user-centered design principles, knowledge of interaction design, usability testing, communication skills.
3. **Web Developer**
   - **Description:** Web developers are responsible for building and maintaining websites using programming languages such as HTML, CSS, and JavaScript. They collaborate with designers to bring the visual aspects of a website to life and ensure its functionality and performance.
   - **Core Values:** Precision, Problem-solving, Continuous Learning, Collaboration.
   - **Necessary Skills:** Proficiency in HTML, CSS, JavaScript, familiarity with web development frameworks (e.g., React, Angular), understanding of responsive design principles, problem-solving skills, ability to work in a team environment.
4. **Game Designer**
   - **Description:** Game designers are responsible for creating the concept, gameplay mechanics, and overall design of video games. They collaborate with artists, programmers, and writers to develop engaging and immersive gaming experiences.
   - **Core Values:** Creativity, Innovation, Adaptability, Collaboration.
   - **Necessary Skills:** Strong understanding of game mechanics and design principles, proficiency in game development engines (e.g., Unity, Unreal Engine), storytelling skills, problem-solving abilities, teamwork.
5. **Product Designer**
   - **Description:** Product designers are responsible for creating and refining the physical and digital products that we use in our daily lives. They collaborate with cross-functional teams to design products that are aesthetically pleasing, functional, and user-friendly.
   - **Core Values:** User-Centric Design, Innovation, Iteration, Collaboration.
   - **Necessary Skills:** Proficiency in design tools (e.g., CAD software, Adobe Creative Suite), understanding of manufacturing processes, user research, prototyping skills, communication skills.
6. **Digital Marketer (with Design Skills)**
   - **Description:** Digital marketers with design skills are responsible for creating visually appealing content for digital marketing campaigns. They design graphics, videos, and other multimedia assets to engage audiences and drive traffic and conversions.
   - **Core Values:** Creativity, Data-Driven Decision Making, Adaptability, Collaboration.
   - **Necessary Skills:** Proficiency in graphic design software, understanding of digital marketing channels (e.g., social media, email, SEO), analytical skills, creativity, communication skills. Certainly! Here are more jobs in art, design, and technology along with their descriptions, core values, and necessary skills:
7. **Art Director**
   - **Description:** Art directors are responsible for the visual style and imagery in magazines, newspapers, product packaging, and movie and television productions. They oversee the work of other designers and artists to ensure that their artistic vision is fulfilled.
   - **Core Values:** Leadership, Creativity, Visionary Thinking, Collaboration.
   - **Necessary Skills:** Strong design skills, leadership abilities, project management skills, communication skills, ability to work under pressure and meet deadlines.
8. **Motion Graphics Designer**
   - **Description:** Motion graphics designers create animated graphics and visual effects for television, film, video games, and digital media. They combine animation, typography, and sound design to create visually engaging content.
   - **Core Values:** Creativity, Attention to Detail, Technical Proficiency, Collaboration.
   - **Necessary Skills:** Proficiency in animation software (e.g., Adobe After Effects, Cinema 4D), understanding of motion design principles, storytelling skills, ability to work in a team environment.
9. **User Researcher**
   - **Description:** User researchers are responsible for gathering insights about user behaviors, needs, and preferences to inform the design of products and services. They conduct qualitative and quantitative research studies, analyze data, and present findings to stakeholders.
   - **Core Values:** Empathy, Analytical Thinking, Curiosity, Collaboration.
   - **Necessary Skills:** Knowledge of research methodologies (e.g., surveys, interviews, usability testing), data analysis skills, empathy for users, communication skills, ability to work collaboratively.
10. **Creative Director**
    - **Description:** Creative directors oversee the creative team and develop the overall vision for advertising campaigns, branding initiatives, and other creative projects. They provide guidance and direction to ensure that the creative output aligns with the client's objectives.
    - **Core Values:** Leadership, Innovation, Strategic Thinking, Collaboration.
    - **Necessary Skills:** Strong creative abilities, leadership skills, strategic thinking, project management skills, communication skills.
11. **Virtual Reality (VR) Designer**
    - **Description:** VR designers create immersive virtual experiences for various applications, including gaming, training, and simulation. They design virtual environments, interactions, and user interfaces to provide users with engaging and realistic experiences.
    - **Core Values:** Innovation, User-Centric Design, Technical Proficiency, Collaboration.
    - **Necessary Skills:** Proficiency in VR development tools (e.g., Unity, Unreal Engine), understanding of VR design principles, 3D modeling and animation skills, problem-solving abilities, teamwork.
12. **Digital Illustrator**
    - **Description:** Digital illustrators create digital artwork for various purposes, including books, magazines, websites, and advertisements. They use digital drawing tablets and software to create illustrations and graphics that convey specific messages or concepts.
    - **Core Values:** Creativity, Attention to Detail, Technical Proficiency, Communication.
    - **Necessary Skills:** Proficiency in illustration software (e.g., Adobe Illustrator, Procreate), strong drawing skills, understanding of composition and color theory, ability to work collaboratively and take direction.
Certainly! Here are more jobs in art, design, and technology along with their descriptions, core values, and necessary skills:
13. **Creative Technologist**
    - **Description:** Creative technologists bridge the gap between technology and creative design by conceptualizing and implementing innovative solutions. They explore new technologies, prototype ideas, and create interactive experiences that merge artistry with technical functionality.
    - **Core Values:** Innovation, Collaboration, Experimentation, Problem-solving.
    - **Necessary Skills:** Proficiency in programming languages (e.g., JavaScript, Python), understanding of design principles, familiarity with emerging technologies (e.g., AR/VR, AI), prototyping skills, ability to collaborate with cross-functional teams.
14. **3D Modeler**
    - **Description:** 3D modelers create three-dimensional models and animations for use in video games, films, television shows, and other multimedia projects. They use specialized software to design and render objects, characters, and environments with a high level of detail and realism.
    - **Core Values:** Attention to Detail, Creativity, Technical Proficiency, Collaboration.
    - **Necessary Skills:** Proficiency in 3D modeling software (e.g., Autodesk Maya, Blender), understanding of anatomy and form, texture mapping and UV unwrapping skills, teamwork, problem-solving abilities.
15. **Artificial Intelligence (AI) Ethicist**
    - **Description:** AI ethicists analyze the ethical implications of AI technologies and provide guidance on responsible AI development and deployment. They address issues such as bias, privacy, transparency, and accountability to ensure that AI systems are designed and used ethically.
    - **Core Values:** Ethics, Critical Thinking, Collaboration, Advocacy.
    - **Necessary Skills:** Knowledge of ethics, philosophy, and social sciences, understanding of AI technologies and their societal impact, communication skills, ability to collaborate with interdisciplinary teams.
16. **Environmental Graphic Designer**
    - **Description:** Environmental graphic designers create visual designs for physical spaces such as buildings, parks, and museums. They integrate graphics, signage, wayfinding systems, and environmental elements to enhance the user experience and communicate information effectively.
    - **Core Values:** User-Centric Design, Sustainability, Collaboration, Innovation.
    - **Necessary Skills:** Proficiency in graphic design software, understanding of architectural principles, knowledge of materials and fabrication techniques, collaboration skills, ability to work with diverse stakeholders.
17. **Sound Designer**
    - **Description:** Sound designers are responsible for creating and editing audio elements for various media productions, including films, video games, and virtual reality experiences. They use sound effects, music, and dialogue to enhance storytelling and create immersive auditory experiences.
    - **Core Values:** Creativity, Attention to Detail, Technical Proficiency, Collaboration.
    - **Necessary Skills:** Proficiency in audio editing software (e.g., Pro Tools, Logic Pro), knowledge of sound design principles, understanding of storytelling and narrative structure, collaboration skills, attention to detail.
18. **Interactive Media Designer**
    - **Description:** Interactive media designers create engaging digital experiences that allow users to interact with content in meaningful ways. They design interfaces, interactions, and multimedia elements for websites, mobile apps, kiosks, and interactive installations.
    - **Core Values:** User-Centric Design, Creativity, Technical Proficiency, Collaboration.
    - **Necessary Skills:** Proficiency in design and prototyping tools, understanding of user experience (UX) design principles, knowledge of interactive technologies (e.g., touchscreens, sensors), collaboration skills, problem-solving abilities.
Of course! Here are more jobs in art, design, and technology, along with their descriptions, core values, and necessary skills:
19. **Fashion Designer**
   - **Description:** Fashion designers create clothing, footwear, and accessories. They sketch designs, select fabrics and patterns, and oversee the production process to bring their designs to life.
   - **Core Values:** Creativity, Innovation, Attention to Detail, Adaptability.
   - **Necessary Skills:** Fashion sketching, knowledge of textiles and garment construction, trend forecasting, understanding of fashion history and current trends, communication skills.
20. **Brand Identity Designer**
   - **Description:** Brand identity designers develop visual elements that represent a company's brand, including logos, color schemes, typography, and brand guidelines. They ensure consistency across all brand communications.
   - **Core Values:** Brand Integrity, Creativity, Attention to Detail, Collaboration.
   - **Necessary Skills:** Graphic design skills, understanding of branding principles, knowledge of typography and color theory, ability to interpret and implement brand strategies, communication skills.
21. **Data Visualization Designer**
    - **Description:** Data visualization designers create visual representations of data to help people understand and interpret complex information. They use charts, graphs, maps, and interactive dashboards to present data in an accessible and meaningful way.
    - **Core Values:** Clarity, Accuracy, Creativity, Empathy.
    - **Necessary Skills:** Proficiency in data visualization tools (e.g., Tableau, D3.js), understanding of data analysis and statistics, knowledge of design principles, storytelling skills, collaboration skills.
22. **Creative Writer/Content Creator**
    - **Description:** Creative writers/content creators produce written content for various mediums such as websites, blogs, social media, advertisements, and marketing materials. They use storytelling and persuasive language to engage and inform audiences.
    - **Core Values:** Creativity, Authenticity, Communication, Adaptability.
    - **Necessary Skills:** Exceptional writing skills, ability to tailor content for different audiences and platforms, SEO knowledge, research skills, collaboration skills.
23. **Experience Designer**
    - **Description:** Experience designers focus on designing holistic experiences across multiple touchpoints, including digital and physical interactions. They consider the user journey and strive to create seamless and memorable experiences.
    - **Core Values:** User-Centric Design, Collaboration, Innovation, Empathy.
    - **Necessary Skills:** Understanding of UX/UI design principles, proficiency in design and prototyping tools, empathy for users, ability to think strategically, collaboration skills.
24. **Art Therapist**
    - **Description:** Art therapists use art and creative expression as a therapeutic technique to improve mental, emotional, and physical well-being. They work with clients to explore feelings, reduce stress, and promote self-awareness and personal growth.
    - **Core Values:** Empathy, Compassion, Creativity, Confidentiality.
    - **Necessary Skills:** Understanding of psychology and counseling techniques, creativity, active listening skills, empathy, ability to create a safe and supportive environment.
25. **Digital Marketing Analyst**
    - **Description:** Digital marketing analysts analyze data from digital marketing campaigns to measure performance, identify trends, and make data-driven recommendations for optimizing marketing strategies.
    - **Core Values:** Analytical Thinking, Continuous Learning, Collaboration, Adaptability.
    - **Necessary Skills:** Proficiency in data analysis tools (e.g., Google Analytics, Adobe Analytics), understanding of digital marketing channels, statistical analysis skills, communication skills, ability to work in a team environment. Certainly! Here are additional jobs in art, design, and technology, along with their descriptions, core values, and necessary skills:
26. **Architect**
   - **Description:** Architects design buildings and structures, considering both aesthetics and functionality. They create detailed plans and drawings, oversee construction projects, and ensure that designs meet building codes and regulations.
   - **Core Values:** Creativity, Attention to Detail, Sustainability, Collaboration.
   - **Necessary Skills:** Architectural design skills, proficiency in CAD software (e.g., AutoCAD, Revit), knowledge of building materials and construction techniques, project management skills, communication skills.
27. **Video Game Producer**
   - **Description:** Video game producers oversee the development of video games from concept to release. They coordinate with designers, programmers, artists, and other team members to ensure that projects are completed on time and within budget.
   - **Core Values:** Leadership, Organization, Adaptability, Collaboration.
   - **Necessary Skills:** Project management skills, knowledge of game development processes, communication skills, problem-solving abilities, ability to work under pressure.
28. **Creative Technologist**
   - **Description:** Creative technologists bridge the gap between technology and creative design by conceptualizing and implementing innovative solutions. They explore new technologies, prototype ideas, and create interactive experiences that merge artistry with technical functionality.
   - **Core Values:** Innovation, Collaboration, Experimentation, Problem-solving.
   - **Necessary Skills:** Proficiency in programming languages (e.g., JavaScript, Python), understanding of design principles, familiarity with emerging technologies (e.g., AR/VR, AI), prototyping skills, ability to collaborate with cross-functional teams.
29. **Typography Designer**
   - **Description:** Typography designers specialize in the art and technique of arranging type to make written language legible, readable, and appealing when displayed. They create fonts, design layouts, and select typefaces for various print and digital media.
   - **Core Values:** Attention to Detail, Creativity, Communication, Precision.
   - **Necessary Skills:** Knowledge of typography principles, proficiency in typography design software (e.g., Adobe InDesign, Glyphs), understanding of typeface anatomy and hierarchy, attention to detail, communication skills.
30. **Digital Animator**
   - **Description:** Digital animators create animated sequences for films, television shows, video games, and other multimedia projects. They use computer software to design and manipulate images, characters, and environments to create lifelike motion.
   - **Core Values:** Creativity, Attention to Detail, Technical Proficiency, Collaboration.
   - **Necessary Skills:** Proficiency in animation software (e.g., Autodesk Maya, Adobe Animate), understanding of animation principles, storytelling skills, teamwork, problem-solving abilities.
31. **Design Thinking Facilitator**
   - **Description:** Design thinking facilitators lead workshops and sessions to apply design thinking methodologies to solve complex problems. They guide participants through the process of empathizing with users, defining problems, ideating solutions, prototyping, and testing.
   - **Core Values:** Empathy, Creativity, Collaboration, Iteration.
   - **Necessary Skills:** Knowledge of design thinking methodologies, facilitation skills, empathy for users, creativity, problem-solving abilities, communication skills.
32. **Art Restoration Specialist**
   - **Description:** Art restoration specialists repair and preserve artworks, artifacts, and cultural heritage objects. They assess damages, clean surfaces, repair structural flaws, and apply protective coatings to restore objects to their original condition.
   - **Core Values:** Preservation, Attention to Detail, Technical Expertise, Ethics.
   - **Necessary Skills:** Knowledge of art history and conservation techniques, fine motor skills, attention to detail, patience, hand-eye coordination.
Certainly! Here are more roles in art, design, and technology:
33. **User Interface (UI) Designer**
   - **Description:** UI designers focus on creating visually appealing and intuitive user interfaces for digital products, such as websites, mobile apps, and software applications. They ensure that the interface design enhances user experience and usability.
   - **Core Values:** User-Centric Design, Creativity, Attention to Detail, Collaboration.
   - **Necessary Skills:** Proficiency in design tools (e.g., Sketch, Adobe XD), understanding of UI design principles, knowledge of user experience (UX) design, collaboration skills, problem-solving abilities.
34. **Social Media Manager**
   - **Description:** Social media managers are responsible for developing and implementing social media strategies to increase brand awareness, engage audiences, and drive traffic or sales. They create content, manage social media accounts, and analyze performance metrics.
   - **Core Values:** Creativity, Communication, Adaptability, Analytics.
   - **Necessary Skills:** Strong writing and communication skills, knowledge of social media platforms and trends, content creation skills (text, images, videos), analytical skills, ability to multitask and prioritize.
35. **Experiential Designer**
   - **Description:** Experiential designers create immersive and engaging physical environments or installations that evoke emotional responses and tell stories. They combine elements such as space, light, sound, and interactive technologies to create memorable experiences.
   - **Core Values:** Creativity, Innovation, User Experience, Collaboration.
   - **Necessary Skills:** Spatial design skills, knowledge of sensory elements (lighting, sound, texture), proficiency in design software, understanding of user experience principles, collaboration and project management skills.
36. **E-learning Designer**
   - **Description:** E-learning designers develop educational materials and courses delivered through digital platforms. They create interactive multimedia content, design user interfaces, and implement instructional strategies to facilitate learning.
   - **Core Values:** Education, Innovation, Accessibility, Collaboration.
   - **Necessary Skills:** Instructional design principles, proficiency in e-learning authoring tools (e.g., Articulate Storyline, Adobe Captivate), multimedia design skills (graphics, animations, videos), knowledge of learning management systems (LMS), collaboration skills.
37. **Print Production Manager**
   - **Description:** Print production managers oversee the process of producing printed materials, such as brochures, magazines, packaging, and promotional materials. They coordinate with printers, graphic designers, and clients to ensure that projects are completed on time and within budget.
   - **Core Values:** Attention to Detail, Organization, Collaboration, Quality.
   - **Necessary Skills:** Knowledge of printing processes and techniques, project management skills, communication skills, attention to detail, ability to work under pressure.
38. **Creative Recruiter**
   - **Description:** Creative recruiters are responsible for sourcing, screening, and hiring candidates for creative positions within organizations. They identify talent, build relationships with candidates, and collaborate with hiring managers to fulfill staffing needs.
   - **Core Values:** Talent, Relationship Building, Communication, Integrity.
   - **Necessary Skills:** Understanding of creative roles and industries, networking skills, interviewing skills, communication skills, organizational skills.
39. **Accessibility Specialist**
   - **Description:** Accessibility specialists ensure that digital products and environments are accessible to users with disabilities. They evaluate designs, provide recommendations for accessibility improvements, and advocate for inclusive design practices.
   - **Core Values:** Inclusivity, Empathy, Advocacy, Technical Proficiency.
   - **Necessary Skills:** Knowledge of accessibility guidelines and standards (e.g., WCAG), understanding of assistive technologies, usability testing skills, communication skills, attention to detail.
40. **Industrial Designer**
   - **Description:** Industrial designers develop concepts and designs for manufactured products, such as appliances, furniture, consumer electronics, and vehicles. They consider factors such as aesthetics, functionality, ergonomics, and manufacturability.
   - **Core Values:** Innovation, Functionality, Aesthetics, Problem-solving.
   - **Necessary Skills:** Design skills, proficiency in CAD software, knowledge of manufacturing processes, prototyping skills, communication skills.
Certainly! Here are more roles within the realms of art, design, and technology:
41. **Creative Strategist**
   - **Description:** Creative strategists develop innovative strategies and campaigns to help brands achieve their goals. They conduct research, analyze market trends, and collaborate with creative teams to develop compelling marketing and branding initiatives.
   - **Core Values:** Creativity, Strategic Thinking, Collaboration, Adaptability.
   - **Necessary Skills:** Strategic planning skills, creativity, market research abilities, communication skills, project management skills.
42. **Digital Art Director**
   - **Description:** Digital art directors oversee the visual design and creative direction of digital projects, such as websites, mobile apps, and digital marketing campaigns. They lead design teams, develop concepts, and ensure that designs align with brand objectives.
   - **Core Values:** Creativity, Leadership, Innovation, Collaboration.
   - **Necessary Skills:** Design skills, leadership abilities, proficiency in design software, understanding of digital platforms, communication skills.
43. **Game Tester/QA Analyst**
   - **Description:** Game testers, also known as quality assurance (QA) analysts, evaluate video games to identify bugs, glitches, and usability issues. They playtest games, document defects, and provide feedback to developers to improve game quality.
   - **Core Values:** Attention to Detail, Patience, Problem-solving, Collaboration.
   - **Necessary Skills:** Attention to detail, patience, analytical skills, familiarity with game development processes, communication skills.
44. **Digital Media Producer**
   - **Description:** Digital media producers oversee the creation and distribution of digital content across various platforms, such as websites, social media, and streaming services. They manage projects, coordinate production teams, and ensure that content meets quality standards.
   - **Core Values:** Creativity, Organization, Adaptability, Collaboration.
   - **Necessary Skills:** Project management skills, creative skills, knowledge of digital media platforms, communication skills, problem-solving abilities.
45. **Artificial Intelligence (AI) Designer**
   - **Description:** AI designers develop user interfaces and experiences for AI-powered products and services. They design conversational interfaces, chatbots, and AI-driven interactions that enhance user engagement and usability.
   - **Core Values:** User-Centric Design, Innovation, Ethical Considerations, Collaboration.
   - **Necessary Skills:** Understanding of AI technologies, UI/UX design skills, knowledge of natural language processing (NLP) and machine learning (ML), creativity, collaboration skills.
46. **Exhibition Designer**
   - **Description:** Exhibition designers create immersive and engaging environments for museums, galleries, trade shows, and events. They design layouts, displays, and interactive installations that communicate ideas, narratives, and educational content.
   - **Core Values:** Creativity, Storytelling, Spatial Design, Collaboration.
   - **Necessary Skills:** Spatial design skills, knowledge of exhibition design principles, proficiency in design software, understanding of user experience, collaboration skills.
6:34
47. **Augmented Reality (AR) Developer**
   - **Description:** AR developers create augmented reality experiences for mobile devices, wearable technology, and other platforms. They develop AR applications, games, and interactive experiences that blend digital content with the real world.
   - **Core Values:** Innovation, User Experience, Technical Proficiency, Collaboration.
   - **Necessary Skills:** Proficiency in AR development tools (e.g., Unity, ARKit, ARCore), knowledge of 3D graphics and animation, programming skills (e.g., C#, JavaScript), creativity, collaboration skills.
48. **Digital Marketing Designer**
   - **Description:** Digital marketing designers create visual assets and collateral for digital marketing campaigns, such as banners, social media graphics, email templates, and landing pages. They design materials that align with brand guidelines and marketing objectives.
   - **Core Values:** Creativity, Brand Consistency, Adaptability, Collaboration.
   - **Necessary Skills:** Graphic design skills, proficiency in design software, understanding of digital marketing principles, creativity, collaboration skills.
49. **Film and Video Editor**
   - **Description:** Film and video editors assemble raw footage into cohesive and engaging visual narratives for films, television shows, commercials, and online videos. They select shots, apply transitions and effects, and adjust audio to tell compelling stories.
   - **Core Values:** Creativity, Attention to Detail, Storytelling, Collaboration.
   - **Necessary Skills:** Proficiency in video editing software (e.g., Adobe Premiere Pro, Final Cut Pro), storytelling skills, attention to detail, creativity, collaboration skills.
50. **Virtual Set Designer**
   - **Description:** Virtual set designers create digital environments for film, television, and live broadcasts. They design and render 3D sets, backgrounds, and virtual elements that integrate seamlessly with live-action footage.
   - **Core Values:** Creativity, Technical Proficiency, Collaboration, Adaptability.
   - **Necessary Skills:** Proficiency in 3D modeling and rendering software (e.g., Autodesk Maya, Cinema 4D), understanding of set design principles, knowledge of virtual production workflows, collaboration skills.
Certainly! Here are more roles in art, design, and technology:
51. **Creative Producer**
   - **Description:** Creative producers oversee the creative aspects of projects, from conception to execution. They develop ideas, assemble teams, manage budgets and schedules, and ensure that the final product aligns with the creative vision and objectives.
   - **Core Values:** Leadership, Creativity, Organization, Collaboration.
   - **Necessary Skills:** Project management skills, creative thinking, leadership abilities, communication skills, problem-solving skills.
52. **Storyboard Artist**
   - **Description:** Storyboard artists create visual representations of scripts or narratives for films, animations, or commercials. They illustrate key scenes, camera angles, and action sequences to help directors and production teams visualize the story.
   - **Core Values:** Creativity, Attention to Detail, Storytelling, Collaboration.
   - **Necessary Skills:** Drawing skills, understanding of cinematic language, storytelling abilities, collaboration skills, adaptability.
53. **Web Accessibility Specialist**
   - **Description:** Web accessibility specialists ensure that websites and digital platforms are accessible to users with disabilities. They audit websites for accessibility compliance, provide recommendations for improvements, and advocate for inclusive design practices.
   - **Core Values:** Inclusivity, Empathy, Advocacy, Technical Proficiency.
   - **Necessary Skills:** Knowledge of web accessibility guidelines (e.g., WCAG), experience with assistive technologies, auditing skills, communication skills, attention to detail.
54. **Interactive Exhibit Designer**
   - **Description:** Interactive exhibit designers create engaging and educational experiences for museums, science centers, and cultural institutions. They design interactive exhibits, installations, and multimedia presentations that encourage visitor participation and learning.
   - **Core Values:** Education, Engagement, Creativity, Collaboration.
   - **Necessary Skills:** Design skills, knowledge of interactive technologies, storytelling abilities, project management skills, collaboration skills.
55. **Virtual Reality (VR) Developer**
   - **Description:** VR developers design and develop virtual reality experiences for applications such as gaming, training, simulation, and virtual tours. They create immersive environments, interactions, and experiences that leverage VR technology.
   - **Core Values:** Innovation, User Experience, Technical Proficiency, Collaboration.
   - **Necessary Skills:** Proficiency in VR development tools (e.g., Unity, Unreal Engine), knowledge of 3D graphics and animation, programming skills (e.g., C#, C++), problem-solving abilities, collaboration skills.
56. **Artificial Intelligence (AI) Engineer**
   - **Description:** AI engineers develop and implement artificial intelligence algorithms and systems for various applications, such as natural language processing, computer vision, and machine learning. They design and train AI models to solve complex problems and improve efficiency.
   - **Core Values:** Innovation, Problem-solving, Ethical Considerations, Collaboration.
   - **Necessary Skills:** Programming skills (e.g., Python, Java), knowledge of machine learning algorithms, familiarity with AI frameworks (e.g., TensorFlow, PyTorch), analytical skills, collaboration skills.
57. **Character Designer**
   - **Description:** Character designers create original characters for use in animations, video games, comics, and other media. They develop character concepts, designs, and visual styles that convey personality, emotion, and storytelling.
   - **Core Values:** Creativity, Character Development, Storytelling, Collaboration.
   - **Necessary Skills:** Drawing skills, understanding of anatomy and proportion, storytelling abilities, proficiency in design software, collaboration skills.
58. **UX Researcher**
   - **Description:** UX researchers investigate user behaviors, needs, and preferences to inform the design and development of products and services. They conduct user research studies, analyze data, and generate insights to improve user experiences.
   - **Core Values:** Empathy, Curiosity, Analytical Thinking, Collaboration.
   - **Necessary Skills:** Knowledge of research methodologies (e.g., interviews, surveys, usability testing), data analysis skills, empathy for users, communication skills, collaboration skills.
59. **Creative Consultant**
   - **Description:** Creative consultants provide expert advice and guidance to clients on creative projects, marketing strategies, branding initiatives, and design solutions. They offer insights, recommendations, and creative direction to help clients achieve their objectives.
   - **Core Values:** Expertise, Creativity, Collaboration, Communication.
   - **Necessary Skills:** Industry knowledge, problem-solving abilities, communication skills, creativity, adaptability.
60. **Colorist**
   - **Description:** Colorists enhance the visual quality of images and videos by adjusting color, contrast, and tone. They work in industries such as film, television, animation, and photography to create mood, atmosphere, and visual consistency.
   - **Core Values:** Attention to Detail, Aesthetic Sensibility, Collaboration, Adaptability.
   - **Necessary Skills:** Proficiency in color grading software (e.g., DaVinci Resolve, Adobe Premiere Pro), understanding of color theory, attention to detail, communication skills, collaboration skills.
Certainly! Here are more roles within the realms of art, design, and technology:
61. **Urban Designer**
   - **Description:** Urban designers plan and design the layout, development, and revitalization of urban areas, neighborhoods, and public spaces. They consider factors such as land use, transportation, sustainability, and community needs.
   - **Core Values:** Sustainability, Community Engagement, Aesthetics, Collaboration.
   - **Necessary Skills:** Urban planning knowledge, design skills, proficiency in design software, understanding of zoning regulations and urban policies, collaboration skills.
62. **Voice User Interface (VUI) Designer**
   - **Description:** VUI designers create conversational interfaces for voice-controlled devices and applications, such as smart speakers and virtual assistants. They design voice interactions, dialogue flows, and prompts that facilitate natural and intuitive user interactions.
   - **Core Values:** User-Centric Design, Innovation, Accessibility, Collaboration.
   - **Necessary Skills:** Understanding of natural language processing (NLP), UX/UI design skills, knowledge of VUI design principles, creativity, collaboration skills.
63. **Environmental Designer**
   - **Description:** Environmental designers create immersive and experiential environments that communicate brand identity, tell stories, and evoke emotions. They design physical spaces, installations, and exhibits for retail, hospitality, events, and cultural institutions.
   - **Core Values:** Creativity, Storytelling, Sustainability, Collaboration.
   - **Necessary Skills:** Spatial design skills, knowledge of materials and fabrication techniques, understanding of user experience, project management skills, collaboration skills.
64. **Medical Illustrator**
   - **Description:** Medical illustrators create visual representations of anatomical and medical subjects for use in textbooks, research publications, patient education materials, and multimedia presentations. They combine artistic skills with scientific knowledge to accurately depict biological structures and processes.
   - **Core Values:** Accuracy, Clarity, Education, Collaboration.
   - **Necessary Skills:** Proficiency in illustration software, understanding of anatomy and physiology, research skills, attention to detail, communication skills.
65. **Storyboard Supervisor**
   - **Description:** Storyboard supervisors oversee the storyboard development process for film, animation, or television productions. They provide guidance to storyboard artists, ensure consistency with the director's vision, and collaborate with production teams to achieve storytelling objectives.
   - **Core Values:** Leadership, Collaboration, Attention to Detail, Adaptability.
   - **Necessary Skills:** Storyboarding skills, leadership abilities, communication skills, understanding of cinematic storytelling, collaboration skills.
66. **Experience Architect**
   - **Description:** Experience architects design holistic and immersive experiences that integrate physical and digital elements to engage audiences and create memorable interactions. They consider user needs, brand identity, and spatial design to orchestrate cohesive experiences.
   - **Core Values:** User-Centric Design, Innovation, Collaboration, Creativity.
   - **Necessary Skills:** Experience design skills, knowledge of spatial design principles, understanding of technology integration, collaboration skills, creativity.
67. **Algorithm Designer**
   - **Description:** Algorithm designers develop algorithms and computational techniques to solve complex problems in various domains, such as data science, optimization, cryptography, and artificial intelligence. They design efficient and scalable algorithms to address specific computational challenges.
   - **Core Values:** Problem-solving, Innovation, Precision, Collaboration.
   - **Necessary Skills:** Proficiency in programming languages (e.g., Python, C++), understanding of algorithm design principles, analytical skills, creativity, collaboration skills.
68. **Sustainable Design Consultant**
   - **Description:** Sustainable design consultants advise clients on incorporating sustainable practices and principles into design projects to minimize environmental impact and promote social responsibility. They assess projects, recommend sustainable strategies, and facilitate green building certifications.
   - **Core Values:** Sustainability, Environmental Stewardship, Collaboration, Innovation.
   - **Necessary Skills:** Knowledge of sustainable design principles, understanding of green building standards (e.g., LEED, BREEAM), communication skills, analytical skills, collaboration skills.
69. **Digital Asset Manager**
   - **Description:** Digital asset managers organize, categorize, and manage digital assets, such as images, videos, documents, and design files, for efficient storage, retrieval, and distribution. They develop and implement asset management systems and workflows to support creative projects.
   - **Core Values:** Organization, Efficiency, Collaboration, Attention to Detail.
   - **Necessary Skills:** Knowledge of digital asset management systems, metadata management skills, organizational skills, communication skills, attention to detail.
70. **Creative Coding Specialist**
   - **Description:** Creative coding specialists use programming languages to create interactive and generative artworks, installations, and digital experiences. They combine coding with visual design, animation, and sound to produce innovative and expressive creative projects.
   - **Core Values:** Innovation, Creativity, Technical Proficiency, Collaboration.
   - **Necessary Skills:** Proficiency in coding languages (e.g., Processing, JavaScript), understanding of creative coding frameworks, knowledge of design principles, collaboration skills, creativity.
71. **Art Curator**
   - **Description:** Art curators manage collections of artwork in museums, galleries, and cultural institutions. They research and select artwork for exhibitions, interpret pieces for the public, and oversee the acquisition, preservation, and display of artwork.
   - **Core Values:** Preservation, Education, Cultural Understanding, Collaboration.
   - **Necessary Skills:** Art history knowledge, research skills, curation abilities, communication skills, collaboration skills.
72. **Design Researcher**
   - **Description:** Design researchers investigate user behaviors, preferences, and needs to inform the design process. They conduct qualitative and quantitative research studies, analyze data, and generate insights to guide design decisions and improve user experiences.
   - **Core Values:** Empathy, Curiosity, Analytical Thinking, Collaboration.
   - **Necessary Skills:** Research methodologies, data analysis skills, empathy for users, communication skills, collaboration skills.
73. **Technical Writer**
   - **Description:** Technical writers create documentation and instructional materials for software, products, and processes. They translate technical information into clear and accessible content for end-users, such as user manuals, tutorials, and online help guides.
   - **Core Values:** Clarity, Accuracy, Communication, Adaptability.
   - **Necessary Skills:** Writing skills, technical knowledge, attention to detail, research skills, communication skills.
74. **Media Planner**
   - **Description:** Media planners develop strategic plans for advertising campaigns across various media channels, such as television, radio, print, digital, and social media. They analyze target audiences, negotiate media buys, and allocate budgets to optimize campaign reach and effectiveness.
   - **Core Values:** Strategic Thinking, Data Analysis, Collaboration, Adaptability.
   - **Necessary Skills:** Market research skills, media buying knowledge, data analysis skills, negotiation skills, collaboration skills.
75. **Design Ethnographer**
   - **Description:** Design ethnographers study human behavior, culture, and social contexts to inform design solutions. They conduct ethnographic research, observe users in their natural environments, and uncover insights that shape the design of products, services, and experiences.
   - **Core Values:** Empathy, Cultural Understanding, Collaboration, Innovation.
   - **Necessary Skills:** Ethnographic research methods, observation skills, empathy for users, storytelling abilities, collaboration skills.
76. **Motion Graphics Designer**
   - **Description:** Motion graphics designers create animated visual content for film, television, video games, websites, and multimedia projects. They combine graphic design, animation, and visual effects to produce dynamic and engaging motion graphics.
   - **Core Values:** Creativity, Technical Proficiency, Attention to Detail, Collaboration.
   - **Necessary Skills:** Animation software skills (e.g., Adobe After Effects, Cinema 4D), design skills, understanding of motion principles, attention to detail, collaboration skills.
77. **Design Educator**
   - **Description:** Design educators teach and mentor students in various design disciplines, such as graphic design, industrial design, UX/UI design, and architecture. They develop curriculum, deliver lectures, facilitate workshops, and provide feedback to support student learning and growth.
   - **Core Values:** Education, Mentorship, Creativity, Collaboration.
   - **Necessary Skills:** Subject matter expertise, teaching skills, communication skills, mentorship abilities, collaboration skills.
78. **Social Impact Designer**
   - **Description:** Social impact designers use design thinking and creative problem-solving to address social, environmental, and humanitarian challenges. They collaborate with communities, nonprofits, and government agencies to develop solutions that have a positive impact on society.
   - **Core Values:** Social Responsibility, Empathy, Collaboration, Innovation.
   - **Necessary Skills:** Design thinking skills, empathy for communities, collaboration skills, project management abilities, advocacy skills.
79. **Content Strategist**
   - **Description:** Content strategists develop strategies for creating, organizing, and delivering content across digital platforms. They define content goals, identify target audiences, and plan content initiatives that align with brand objectives and user needs.
   - **Core Values:** Strategy, Creativity, User-Centricity, Collaboration.
   - **Necessary Skills:** Content strategy knowledge, writing skills, analytical skills, understanding of SEO principles, collaboration skills.
80. **Artificial Intelligence (AI) Artist**
   - **Description:** AI artists use artificial intelligence and machine learning algorithms to create artworks, generate visuals, and explore new forms of creative expression. They collaborate with AI researchers and technologists to push the boundaries of art and technology.
   - **Core Values:** Innovation, Creativity, Collaboration, Ethical Considerations.
   - **Necessary Skills:** Understanding of AI technologies, programming skills, creativity, collaboration skills, ethical awareness. New
81. **Data Visualization Specialist**
   - **Description:** Data visualization specialists design and create visual representations of data to help people understand complex information more easily. They use charts, graphs, maps, and interactive dashboards to communicate insights and trends.
   - **Core Values:** Clarity, Accuracy, Creativity, Communication.
   - **Necessary Skills:** Proficiency in data visualization tools (e.g., Tableau, Power BI), knowledge of data analysis and statistics, design skills, storytelling abilities, attention to detail.
82. **Packaging Designer**
   - **Description:** Packaging designers create the visual design and structural packaging for products. They consider factors such as branding, usability, sustainability, and shelf appeal to design packaging that protects products and attracts consumers.
   - **Core Values:** Creativity, Functionality, Sustainability, Branding.
   - **Necessary Skills:** Design skills, knowledge of packaging materials and manufacturing processes, branding knowledge, proficiency in design software, attention to detail.
83. **Artificial Intelligence (AI) Ethics Researcher**
   - **Description:** AI ethics researchers examine the ethical implications of artificial intelligence technologies and algorithms. They explore issues such as bias, fairness, transparency, accountability, and privacy to ensure responsible AI development and deployment.
   - **Core Values:** Ethics, Accountability, Transparency, Social Responsibility.
   - **Necessary Skills:** Research skills, knowledge of AI technologies, understanding of ethical frameworks, critical thinking abilities, communication skills.
84. **Gaming User Researcher**
   - **Description:** Gaming user researchers study player behaviors, preferences, and experiences to inform game design decisions. They conduct playtesting sessions, analyze player feedback, and provide insights to game developers to improve gameplay and user satisfaction.
   - **Core Values:** User-Centric Design, Analytical Thinking, Collaboration, Innovation.
   - **Necessary Skills:** Research methodologies, data analysis skills, understanding of game design principles, communication skills, collaboration skills.
85. **Augmented Reality (AR) Content Creator**
   - **Description:** AR content creators develop augmented reality experiences for various applications, such as education, entertainment, marketing, and training. They design and produce AR content, including 3D models, animations, and interactive elements.
   - **Core Values:** Creativity, Innovation, User Experience, Collaboration.
   - **Necessary Skills:** Proficiency in AR development tools (e.g., Unity, ARKit), 3D modeling and animation skills, design skills, programming knowledge, collaboration skills.
86. **Digital Archivist**
   - **Description:** Digital archivists manage and preserve digital collections of cultural, historical, or organizational materials. They organize digital assets, ensure long-term access and preservation, and provide reference services for researchers and stakeholders.
   - **Core Values:** Preservation, Accessibility, Organization, Collaboration.
   - **Necessary Skills:** Knowledge of archival principles and standards, digital asset management skills, metadata management abilities, communication skills, attention to detail.
87. **Brand Strategist**
   - **Description:** Brand strategists develop strategies to build and manage brands effectively. They conduct market research, analyze competitive landscapes, define brand positioning, and develop brand identities and messaging to create strong brand equity.
   - **Core Values:** Strategy, Creativity, Brand Integrity, Collaboration.
   - **Necessary Skills:** Strategic thinking, market research skills, branding knowledge, communication skills, collaboration skills.
88. **Digital Product Manager**
   - **Description:** Digital product managers oversee the development and management of digital products, such as websites, mobile apps, and software applications. They define product requirements, prioritize features, and collaborate with cross-functional teams to deliver successful products.
   - **Core Values:** User-Centric Design, Leadership, Collaboration, Adaptability.
   - **Necessary Skills:** Product management skills, understanding of UX/UI design principles, technical knowledge, communication skills, problem-solving abilities.
89. **Experiential Marketing Specialist**
   - **Description:** Experiential marketing specialists create immersive brand experiences to engage consumers and build brand loyalty. They develop and execute experiential marketing campaigns, events, and activations that leave a lasting impression on audiences.
   - **Core Values:** Creativity, Engagement, Brand Experience, Collaboration.
   - **Necessary Skills:** Event planning skills, creativity, project management abilities, communication skills, collaboration skills.
90. **Digital Accessibility Consultant**
   - **Description:** Digital accessibility consultants advise organizations on making digital products and services accessible to people with disabilities. They assess digital properties for accessibility compliance, provide recommendations for improvements, and offer training and support to ensure inclusivity.
   - **Core Values:** Inclusivity, Empathy, Advocacy, Technical Proficiency.
   - **Necessary Skills:** Knowledge of accessibility guidelines (e.g., WCAG), understanding of assistive technologies, auditing skills, communication skills, advocacy skills.
91. **User Experience (UX) Architect**
   - **Description:** UX architects design the overall structure and flow of digital products and experiences to ensure intuitive user interactions and seamless navigation. They create wireframes, user flows, and prototypes to define the user experience.
   - **Core Values:** User-Centric Design, Information Architecture, Collaboration, Adaptability.
   - **Necessary Skills:** UX/UI design skills, knowledge of information architecture principles, proficiency in design and prototyping tools (e.g., Sketch, Adobe XD), collaboration skills, problem-solving abilities.
92. **Film Director**
   - **Description:** Film directors oversee all aspects of the filmmaking process, from script development and casting to production and post-production. They guide actors, make creative decisions, and ensure that the final film aligns with their vision.
   - **Core Values:** Visionary Leadership, Storytelling, Collaboration, Adaptability.
   - **Necessary Skills:** Creative vision, leadership abilities, communication skills, understanding of cinematic techniques, collaboration skills.
93. **3D Modeler**
   - **Description:** 3D modelers create three-dimensional models and assets for use in films, video games, animation, and virtual reality experiences. They sculpt, texture, and rig digital characters, objects, and environments using specialized software.
   - **Core Values:** Attention to Detail, Creativity, Technical Proficiency, Collaboration.
   - **Necessary Skills:** Proficiency in 3D modeling software (e.g., Autodesk Maya, Blender), understanding of anatomy and form, texturing and shading skills, collaboration skills.
94. **Digital Marketing Analyst**
   - **Description:** Digital marketing analysts analyze marketing data and metrics to evaluate the performance of digital campaigns and initiatives. They track key performance indicators, conduct market research, and provide insights to optimize marketing strategies.
   - **Core Values:** Data-Driven Decision Making, Analytical Thinking, Collaboration, Adaptability.
   - **Necessary Skills:** Data analysis skills, proficiency in analytics tools (e.g., Google Analytics, Adobe Analytics), knowledge of digital marketing principles, communication skills, collaboration skills.
95. **Human-Computer Interaction (HCI) Designer**
   - **Description:** HCI designers focus on creating interfaces and interactions between humans and computers that are intuitive, efficient, and user-friendly. They apply principles from psychology, ergonomics, and usability to design interfaces that meet user needs.
   - **Core Values:** User-Centric Design, Empathy, Collaboration, Innovation.
   - **Necessary Skills:** Knowledge of HCI principles, UX/UI design skills, prototyping skills, understanding of human psychology, collaboration skills.
96. **Cartoonist**
   - **Description:** Cartoonists create humorous or satirical illustrations, comics, and cartoons for print publications, websites, and social media. They develop unique visual styles and use storytelling techniques to convey messages and entertain audiences.
   - **Core Values:** Creativity, Humor, Visual Communication, Adaptability.
   - **Necessary Skills:** Drawing skills, storytelling abilities, creativity, adaptability, digital illustration skills.
97. **Virtual Production Specialist**
   - **Description:** Virtual production specialists use virtual production techniques, such as motion capture, real-time rendering, and virtual sets, to create immersive visual experiences for film, television, and interactive media.
   - **Core Values:** Innovation, Collaboration, Technical Proficiency, Adaptability.
   - **Necessary Skills:** Knowledge of virtual production workflows, proficiency in virtual production tools (e.g., Unreal Engine, MotionBuilder), understanding of cinematography, collaboration skills, problem-solving abilities.
98. **Design Language Specialist**
   - **Description:** Design language specialists develop and maintain design systems and visual languages that define the overall look and feel of products and brands. They establish design guidelines, components, and patterns to ensure consistency and coherence across platforms and experiences.
   - **Core Values:** Consistency, Collaboration, User Experience, Innovation.
   - **Necessary Skills:** Design system management skills, knowledge of design principles, proficiency in design tools, communication skills, collaboration skills.
99. **Creative Technology Director**
   - **Description:** Creative technology directors lead interdisciplinary teams to conceptualize and implement innovative technological solutions for creative projects. They bridge the gap between technology and artistry to deliver cutting-edge experiences.
   - **Core Values:** Innovation, Leadership, Collaboration, Creativity.
   - **Necessary Skills:** Technical expertise, leadership abilities, project management skills, creativity, collaboration skills.
100. **Artificial Intelligence (AI) Composer**
   - **Description:** AI composers use artificial intelligence algorithms to generate music compositions autonomously or in collaboration with human composers. They explore AI-generated music as a new form of creative expression.
   - **Core Values:** Innovation, Creativity, Collaboration, Ethical Considerations.
   - **Necessary Skills:** Knowledge of AI technologies, understanding of music theory, programming skills, creativity, collaboration skills.
"""

def query_openai(transcript):
    client = OpenAI(
    api_key=os.getenv("OAI_API_KEY"))
    head = "Here's some information about me:"
    prompt = "Based on what I told you about me, suggest me 3 jobs that are fit for me using the following data:"

    completion = client.chat.completions.create(
        messages=[
            {
                "role": "user",
                "content": f'{head} {transcript} {prompt} {data}',
            }
        ],
        model="gpt-3.5-turbo"
    )

    return completion.json()

def prune_audio_file():    
    if os.path.exists("./extracted_audio.mp3"):
        os.remove("./extracted_audio.mp3")

def transcribe():
    aai.settings.api_key = os.getenv("AAI_API_KEY")

    FILE_URL = "./extracted_audio.mp3"

    transcriber = aai.Transcriber()
    transcript = transcriber.transcribe(FILE_URL)

    if transcript.status == aai.TranscriptStatus.error:
        print(transcript.error)
    else:
        return transcript.text

app = Flask(__name__)
CORS(app)

@app.route('/upload', methods=['POST'])
def upload():
    prune_audio_file()
    try:
        audio_file = request.files['audio']
        
        audio_file.save("extracted_audio.mp3")
        print("Audio file saved as: extracted_audio.mp3")
        
        transcript = transcribe()
        jobs = query_openai(transcript)
        
        return jsonify({'suggestions': jobs})
    except Exception as e:
        return jsonify({'error': str(e)}), 500

if __name__ == '__main__':
    app.run(debug=True)
