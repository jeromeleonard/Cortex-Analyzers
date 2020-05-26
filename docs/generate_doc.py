#!/usr/bin/env python3
# -*- coding: utf-8 -*

"""
This programs aims at generating documentation for analyzers and responders by reading .json file of each neuron and generate associated .md file based upon output_page.md samples.


docs/index.md
docs/analyzers/NAME/flavor.md
docs/responders/NAME/flavor.md
"""

from os import listdir, chdir, path, makedirs
from shutil import copy
import markdown
from mdutils.mdutils import MdUtils
from mdutils import Html
import json


def neuron2md(nt,neuron, doc_path):
  """
  name: str (analyzers or responders)
  neuron: str
  doc_path: str
  """

  # Title 
  neuron_path = "{}/{}".format(nt,neuron)
  mdFile = MdUtils(file_name="{}.md".format(neuron),title="")
  mdFile.new_header(level=1, title=neuron)

    # Analyzers or Responders flavors
  for f in listdir(neuron_path):
    if nt in ["analyzers", "responders"] and f.endswith(".json"):
      with open("{}/{}".format(neuron_path, f),'r') as fc:
        config = json.load(fc)
        # Logo
        if config.get('service_logo'):
          logo_path = config.get('service_logo').get('path')
          logo_src_path = "{}/{}".format(neuron_path,config.get('service_logo').get('path'))
          if path.exists(logo_src_path):
            ext = logo_path.split('.')[-1]
            logo_md_path = "assets/{}_logo.{}".format(f.split('.')[0],ext)
            logo_dest_path = "{}/{}/{}".format(doc_path,nt,logo_md_path)
            copy(logo_src_path, logo_dest_path)
            mdFile.new_line(mdFile.new_inline_image(text="service_logo", path=logo_md_path))

        mdFile.new_line()

        # Description and README.md file 
        if 'README.md' in listdir(neuron_path):
          readme = open("{}/README.md".format(neuron_path), 'r')
          mdFile.new_paragraph(readme.read())
          readme.close

        mdFile.new_header(level=2, title=config.get('name'))
        mdFile.new_line("**Author**: _{}_".format(config.get('author')))
        mdFile.new_line("**License**: _{}_".format(config.get('license')))
        mdFile.new_line("**Version**: _{}_".format(config.get('version')))
        mdFile.new_line("**Supported observables types**: _{}_".format(config.get('dataTypeList')))
        mdFile.new_line("**Registration required**: \
          _{}_".format(config.get('registration_required','N/A')))
        mdFile.new_line("**Subscription required**: \
          _{}_".format(config.get('subscription_required','N/A')))
        mdFile.new_line("**Free subscription**: \
          _{}_".format(config.get('free_subscription','N/A')))
        mdFile.new_line('**Third party service**: '+\
          mdFile.new_inline_link(link=config.get('service_homepage', 'N/A'), text=config.get('service_homepage', 'N/A')))
        
        mdFile.new_line()
        mdFile.new_header(level=3, title='Description')
        mdFile.new_paragraph(config.get('description', 'N/A'))
    
      
        mdFile.new_line()
        mdFile.new_header(level=3, title='Configuration')
        
        if config.get('configurationItems') and len(config.get('configurationItems')) > 0:
          for c in config.get('configurationItems'):
            configuration_items = ["**{}**".format(c.get('name')), c.get('description', 'No description')]
            configuration_items.extend(["**Default value if not configured**",  "_{}_".format(c.get('default', 'N/A'))])
            configuration_items.extend(["**Type of the configuration item**",  "_{}_".format(c.get('type'))])
            configuration_items.extend(["**The configuration item can contain multiple values**",  "_{}_".format(c.get('multi'))])
            configuration_items.extend(["**Is required**",  "_{}_".format(c.get('required'))])
            mdFile.new_line()
            mdFile.new_table(columns=2, rows=5, text=configuration_items, text_align='left')

        else:
          mdFile.new_paragraph("No specific configuration required.")
    
    
    # Analysers report samples 
    if nt == "analyzers" and f.endswith(".json"):
      # Templates for TheHive
      mdFile.new_line()
      mdFile.new_header(level=3, title='Templates samples for TheHive')

      ## Copy images files to destination folder
      base_neuronname = f.split('.')[0]
      if config.get('screenshots'):
              # if config.get('thehive_short_report') or config.get('thehive_long_report'):
        for idx, sc in enumerate(config.get('screenshots')):
          sc_path = sc.get('path')
          sc_src_path = "{}/{}".format(neuron_path,sc.get('path'))
          if path.exists(sc_src_path):
            sc_filename = path.basename(sc.get('path'))
            ext = sc_filename.split('.')[-1]
            sc_md_path = "assets/{}_{}.{}".format(base_neuronname,idx,ext)
            sc_dest_path ="{}/{}/{}".format(doc_path,nt,sc_md_path)
            copy(sc_src_path, sc_dest_path)
            mdFile.new_paragraph(mdFile.new_inline_image(text=sc.get('caption','screenshot'), path=sc_md_path))
      else:
        mdFile.new_paragraph("No template samples to display.")

  # Save md file
  dest_dir = "{}/{}".format(doc_path, nt)
  if not path.exists(dest_dir):
    makedirs(dest_dir)
  olddir = path.abspath(path.curdir)
  chdir(dest_dir)
  mdFile.create_md_file()
  chdir(olddir)
 


def run():
  #import argparse
  doc_path = "./docs/docs" 
  #parser = argparse.ArgumentParser()
  #parser.add_argument("dp", help="doc path")
  #args = parser.parse_args()

  for nt in ["analyzers", "responders"]:
    if  path.exists("./{}".format(nt)):
      #nt = "./{}".format(nt)
      for neuron in listdir(nt):
        neuron2md(nt, neuron, doc_path)


if __name__ == '__main__':
  run()
