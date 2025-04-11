from language_lists import language_samples_url, all_languages

all_languages = list(set(all_languages))
langs = [lang.lower() for (code, lang) in all_languages]

for lang in langs:
  if lang not in language_samples_url.keys():
    language_samples_url[lang] = "N/U"

def get_samples_text(job_details):
  job_details = " ".join(job_details.split())
  job_details = job_details.lower()
  job_details_text = " " + job_details + " "
  job_text = ""

  for job_details_char in job_details_text:
    if (job_details_char >= "a" and job_details_char <= "z") or (job_details_char >= "0" and job_details_char <= "9"):
      job_text += job_details_char
    else:
      job_text += " "
  job_details = job_text
  # print(job_details)
  samples_text = ""
  if "subtitl" in job_details or "caption" in job_details or "srt" in job_details:
    languages = list(language_samples_url.keys())
    matched_languages = []
    extra_languages = []

    for language in languages:
      lang = " " + language + " "
    
      if lang in job_details:
        matched_language = language_samples_url[language]
    
        if matched_language == "es" or matched_language == "spanish":
          if "latin american" in job_details or "latin" in job_details:
            matched_language = "la-" + matched_language
        
        if matched_language == "N/U": extra_languages.append(lang[1:-1])

        else: matched_languages.append(matched_language)
    # print(matched_languages)
    matched_languages = list(set(matched_languages))
    if len(matched_languages) > 0:
      samples_text = "Samples of subtitling work:\n"

      for language in matched_languages:
        samples_text += language + "\n\n" 
      
      if len(extra_languages) and len(matched_languages):
        samples_text += f"We are unable to share subtitling samples in {extra_languages[0]} language because of NDA’s signed with previous clients.\n\n"

  return samples_text