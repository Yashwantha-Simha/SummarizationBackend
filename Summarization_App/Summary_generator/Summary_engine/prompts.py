
from ctypes import pointer


classificaton_prompts= {
    "Prompt 1": '''Please classify the above pharma content into any one of the following classes,
                classes = ["Approval", "Phase 3 Data Release", "Filing"]
                please note that I want you to classify/ categorize it into only 1 category, not multiple. Always respond with only the category as an output, nothing extra.

                The classification rules are as below:
                Approval: If the communication includes information about actual regulatory approval of a drug, treatment, or therapy by a governing body (e.g., FDA approval).
                Phase 3 Data Release: If the communication includes detailed information regarding finalized results and comprehensive analyses from Phase 3 clinical trials in. If the content covers information regarding Phase III trial results disclosure, study results, impact analysis, phase 3 trial outcomes, efficacy results and safety data, study enrollment, treatment groups,  safety profiles,  primary endpoint achievement, and regulatory steps, any other information that have been disclosed after the phase 3 trial's completion.
                Filing: If the communication includes information about filing and submission of applications but it is not yet approved.''',
    "Prompt 2": '''Please classify the above pharma content into any one of the following classes,
                classes = ["Phase 3 Data Release", "Approval", "Phase 3 Data Announcement", "Filing Announcement"]
                please note that I want you to classify/ categorize it into only 1 category, not multiple. Always respond with only the category as an output, nothing extra.

                The classification rules are as below:
                Approval: If the communication includes information about actual regulatory approval of a drug, treatment, or therapy by a governing body (e.g., FDA approval).
                Phase 3 Data Release: If the communication includes detailed information regarding finalized results and comprehensive analyses from Phase 3 clinical trials in. If the content covers information regarding Phase III trial results disclosure, study results, impact analysis, phase 3 trial outcomes, efficacy results and safety data, study enrollment, treatment groups,  safety profiles,  primary endpoint achievement, and regulatory steps, any other information that have been disclosed after the phase 3 trial's completion.
                Phase 3 Data Announcement: If the communication includes information about intention to conduct a global Phase III study, upcoming Data Presentation of phase 3, plans about Phase 3 trials rather than the detailed outcomes of the Phase 3 trials, interim analyses, Anticipation/ expectations of Future Events, updates on the initiation of Phase 3, plans to initiate a Phase 3 combination, details of Presentation Schedules,  Preliminary Analysis that is results of the Phase 2 trial.
                Filing Announcement: If the communication includes information about Intent to Obtain Approval but No Confirmation of Approval or intent to file for approval.''',
    "Prompt 3": '''Please analyze the provided pharmaceutical content and determine its appropriate category from the following options:

                Approval: If the content pertains to the regulatory approval of a drug, treatment, or therapy by a governing body (e.g., FDA approval).
                Phase 3 Data Release: If the content includes detailed information about Phase 3 trial results, efficacy, and safety profiles that have been disclosed after the trial's completion.
                Phase 3 Data Announcement: When the content indicates that data from a Phase 3 trial will be released or presented in the future, providing advance notice of the upcoming release.
                Filing Announcement: If the content is about the intent to file for approval but not necessarily the actual approval.
                Please assign only one category to the provided content based on these rules.''',
    "Prompt 4": '''Given the following pharmaceutical content, please categorize it into the most appropriate class from the options below:

                Approval: If the content relates to the actual regulatory approval of a drug, treatment, or therapy by a governing body (e.g., FDA approval).
                Phase 3 Data Release: If the content includes detailed information about Phase 3 trial results, efficacy, and safety profiles that have been disclosed after the trial's completion.
                Phase 3 Data Announcement: When the content indicates that data from a Phase 3 trial will be released or presented in the future, providing advance notice of the upcoming release.
                Filing Announcement: If the content is about the intent to file for approval but not necessarily the actual approval.
                Please assign only one category to the provided content based on these rules to ensure the most accurate result.''',
    "Prompt 5": '''Please assign an appropriate category from the listed classification options to the pharmaceutical content provided above.
                The categories include: ""Phase 3 Data Release"", ""Approval"", ""Phase 3 Data Announcement"", and ""Filing Announcement"". Each content should only be assigned to a single category.

                These categories are defined as follows:
                "Approval" corresponds to the official approval of a medication, treatment, or therapy by a regulatory authority, such as the FDA.
                "Phase 3 Data Release" pertains to detailed disseminations about Phase 3 trial results, including efficacy and safety profiles, disclosed upon the conclusion of the trial.
                "Phase 3 Data Announcement" refers to a pre-announcement that Phase 3 trial data will be presented or released in future, indicating an impending disclosure.
                "Filing Announcement" stands for the declaration of intention to apply for approval, although it does not guarantee actual approval.
                Please ensure that each content snippet is categorized under exactly one category.''',
    "Prompt 6_reason": '''Please classify the above pharma content into any one of the following classes,
                classes = ["Approval", "Phase 3 Data Release", "Filing"]
                please note that I want you to classify/ categorize it into only 1 category, not multiple. Give the category, followed by an underscored followed by only a sinle line expanation as to why you have categgorized so..

                The classification rules are as below:
                Approval: If the communication includes information about actual regulatory approval of a drug, treatment, or therapy by a governing body (e.g., FDA approval).
                Phase 3 Data Release: If the communication includes detailed information regarding finalized results and comprehensive analyses from Phase 3 clinical trials in. If the content covers information regarding Phase III trial results disclosure, study results, impact analysis, phase 3 trial outcomes, efficacy results and safety data, study enrollment, treatment groups,  safety profiles,  primary endpoint achievement, and regulatory steps, any other information that have been disclosed after the phase 3 trial's completion.
                Filing: If the communication includes information about filing and submission of applications but it is not yet approved.''',
    "Prompt 7_na": '''Please classify the above pharma content into any one of the following classes,
                classes = ["Approval", "Phase 3 Data Release", "Filing", "NA"]
                please note that I want you to classify/ categorize it into only 1 category, not multiple. Always respond with only the category as an output, nothing extra.

                The classification rules are as below:
                Approval: If the communication includes information about actual regulatory approval of a drug, treatment, or therapy by a governing body (e.g., FDA approval).
                Phase 3 Data Release: If the communication includes detailed information regarding finalized results and comprehensive analyses from Phase 3 clinical trials in. If the content covers information regarding Phase III trial results disclosure, study results, impact analysis, phase 3 trial outcomes, efficacy results and safety data, study enrollment, treatment groups,  safety profiles,  primary endpoint achievement, and regulatory steps, any other information that have been disclosed after the phase 3 trial's completion.
                Filing: If the communication includes information about filing and submission of applications but it is not yet approved.
                NA: If you are not very clear about the classififation, please classify it as NA.''',
    "Prompt_summary_var": lambda points_words, Summary_type, importance, exclude, additional_info: f'''As a pharma Competitive Intelligence summarizer, your primary objective is to provide a concise summary of the provided pharma content. Focus specifically on {importance}. Summarize key points, news, highlights, data, developments, and updates ONLY. Disregard non-essential details like {exclude} , company commitments, website references, and information about the companies' focus areas unless directly related to the specified topics. Summarize in {points_words} {Summary_type} , ensuring no critical data is omitted, and refrain from fabricating information. Maintain the original flow while omitting unnecessary context and promotional content {additional_info}.''',
"Prompt_summary_by_content_id": lambda words,importance,exclude :  f'''As a pharma Competitive Intelligence summarizer, your primary objective is to provide a concise {words} word summary of the provided pharma content. Focus specifically on 
{importance}. Summarize key points, news, highlights, data, developments, and updates ONLY. Disregard non-essential details like {exclude} , company commitments, website references, and information about the companies' focus areas unless directly related to the specified topics. Summarize in bullet points, ensuring no critical data is omitted, and refrain from fabricating information. Maintain the original flow while omitting unnecessary context and promotional content.''',
    "Prompt_summary": '''As a Competitive Intelligence summarizer specialized in pharmaceuticals, please create a concise 100-150 word summary from the perspective of Merck and Keytruda. Highlight key points, recent news, developments, and updates related to these entities. Organize the summary into bullet points to maintain clarity and coherence. Exclude extraneous details like contact information, forward-looking statements, and company specifics. Ensure comprehensive coverage without fabricating information or omitting essential data''',
    "Prompt_er":'''You are a smart and intelligent Entity Recognition system. I will provide you the definition of the entities you need to extract and the sentence from where it should be extracted, provide 'NA' if any of it is not available.
                    Entity Definition:
                    1. Drug/moelcule name: Name of only one drug or molecule that the text is peaking about.
                    2. Company name: Name of the manufacturing company of the drug/molecule, only one company name.
                    2. DATE: Any format of dates. Dates can also be in natural language, only one date.''',
    "Prompt_3_point": '''what are the important dates provided in the artcile?''',
	"Prompt_5_point": '''As a Competitive Intelligence summarizer specialized in pharmaceuticals, summarize the provided content in just 5 points'''
}


multilevel_prompts  = {
    "Prompt level 1": '''Please classify the above content into any one of the following classes,
                classes = ["Pharma", "Non Pharma"]
                Please note that I want you to classify/categorize it into only 1 category, not multiple. The output should just be the category and nothing extra

                The classification rules are as below:
                Non Pharma: If the content is not related to pharma.
                Pharma: If the communication is related to pharma like drugs, molecules, trial, phases, etc.''',
    "Prompt level 2": '''Please classify the above content into any one of the following classes,
                classes = ["Clinical Trial Information", "Regulatory status", "NA"]
                Please note that I want you to classify/categorize it into only 1 category, not multiple. The output should just be the category and nothing extra.

                Clinical Trial Information: If the content pertains to clinical trials. information regarding phases, trials like safety, efficacy etc..
                Regulatory status: If the content pertains to the regulatory aspects.
                NA: If you are not sure about the classification.''',
    "Prompt level 3": '''Please classify the above content into any one of the following classes,
                 classes = ["Phase 2", "Phase 3", "NA"] 
                 Please note that I want you to classify/categorize it into only 1 category, not multiple. The output should just be the category and nothing extra

                 The classification rules are as below:
                 Phase 2: If the content is related to Phase 2 clinical trials.
                 Phase 3: If the content is related to Phase 3 clinical trials.
                 NA: If you are not sure about the classification.''',
    "Prompt level 4": '''Please classify the above content into any one of the following classes,
                 classes = ["Phase 3 Data Release", "Approval", "NA"] 
                 Please note that I want you to classify/categorize it into only 1 category, not multiple. The output should just be the category and nothing extra

                 The classification rules are as below:
                 Phase 3 Data Release: If the communication includes detailed information regarding finalized results and comprehensive analyses from Phase 3 clinical trials in. If the content covers information regarding Phase III trial results disclosure, study results, impact analysis, phase 3 trial outcomes, efficacy results and safety data, study enrollment, treatment groups,  safety profiles,  primary endpoint achievement, and regulatory steps, any other information that have been disclosed after the phase 3 trial's completion.
                 Approval: If the communication includes information about actual regulatory approval of a drug, treatment, or therapy by a governing body (e.g., FDA approval)
                 NA: If you are not sure about the classification.''',
    "Prompt level 5": '''Please classify the above content into any one of the following classes,
                 classes = ["Phase 3 Data Announcement", "Actual Filing", "NA"] 
                 Please note that I want you to classify/categorize it into only 1 category, not multiple. The output should just be the category and nothing extra

                 The classification rules are as below:
                 Phase 3 Data Announcement: If no actual data is disclosed in the communication but  just say that the data will be presented in an upcoming conference or later.
                 Actual Filing : Actual filing of the product.
                 NA: If you are not sure about the classification.'''
}
