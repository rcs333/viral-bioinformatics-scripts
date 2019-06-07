#!/usr/bin/env python3

import argparse
import sys
import numpy as np
import pandas as pd
from bokeh import events
from bokeh.io import export_png, save
from bokeh.resources import CDN
from bokeh.embed import components, file_html, autoload_static
from bokeh.plotting import figure, show, output_file
from bokeh.models import ColumnDataSource, Jitter, BoxAnnotation, DataRange1d, HoverTool, CategoricalTicker, Slider, CustomJS, Label, WheelZoomTool, ResetTool, Button, TextInput
from bokeh.models.tickers import FixedTicker
from bokeh.transform import jitter, factor_cmap
from bokeh.models.widgets import Panel, Tabs, Paragraph, Div, CheckboxGroup
from bokeh.layouts import column, layout, widgetbox, row
from palette import color_palette
import subprocess

# Uses info from protein.csv to shade every other protein in light green, and annotate with protein names.
def protein_annotation(first):
	protein_locs = []
	protein_names = []	

	# Shades in every other protein region. Provides warning if proteins overlap.
	for i in range(0, proteins.shape[0]):
		if(i==0):
			x1 = 0
		elif(proteins.iloc[i,1] < proteins.iloc[i-1,2]) and first:
			print('WARNING: Protein-' + str(proteins.iloc[i,0]) + ' is overlapping with Protein-' + str(proteins.iloc[i-1,0]))
			print('Analysis will continue but the visualization for these two proteins will look a little funny. Often the fix for this is simply deleting the small ancilary proteins that overlapping from the gff file and using the -f and -g flags. For more help see the readme.')
			x1 = proteins.iloc[i,1]
		else:
			x1 = proteins.iloc[i,1]
		if(i==proteins.shape[0]-1):
			x2 = proteins.iloc[i,2]
		else:
			x2 = proteins.iloc[(i+1),1]
		if(i%2==0):
			genome_plot.add_layout(BoxAnnotation(left=x1, right=x2, fill_alpha=0.1, fill_color='green'))
		protein_locs.append((x1+x2)/2)
		protein_names.append(proteins.iloc[i,0])

	# Adds protein labels as tick marks.
	genome_plot.xaxis.ticker = protein_locs
	protein_locs2 = []
	for protein_loc in protein_locs:
		str_protein_loc = str(protein_loc)
		## print("old str_protein_loc" + str_protein_loc)
		if ".0" in str_protein_loc:
			str_protein_loc = str_protein_loc.split('.')[0]
			## print("split" + str_protein_loc)
			protein_locs2.append(int(str_protein_loc))
		else:
			protein_locs2.append(float(str_protein_loc))	
	genome_plot.xaxis.major_label_overrides = dict(zip(protein_locs2, protein_names))
	return protein_names

	
# Creates the legend and configures some of the toolbar stuff.
def configurePlot(g):
	g.legend.location = "top_right"
	# Adjusts size of scatter points within legend.
	g.legend.glyph_width = 35
	g.legend.glyph_height = 35
	# Adjusts visual properties of legend.
	g.legend.spacing = -10
	g.legend.background_fill_alpha = 0.5
	## disabled scroll wheel zooming for all plots - RCS
	## g.toolbar.active_scroll = g.select_one(WheelZoomTool)

	#Adjusts tick visualization.
	g.yaxis.axis_label_standoff = 10
	g.yaxis.axis_label = "Allele Frequency (%)"
	g.xaxis.minor_tick_line_color = None

# Callback for the sliders and the checkboxes for non/synonymous mutations.
# Goes through data and selects/pushes the data with the matching criteria.
def sliderCallback(ref_source, source, slider, slider_af, syngroup, muts):
	return CustomJS(args=dict(ref=ref_source, depth_sample=source, slider=slider, slider_af=slider_af, checkbox=syngroup, muts=unique_longitudinal_muts), code = """
		let depth = slider.value;
		let af = slider_af.value;
		let colnames = Object.keys(ref.data);
		for (let a = 0; a < colnames.length; a++) {
			depth_sample.data[colnames[a]] = [];
		}
		if (checkbox.active.indexOf(0)>-1) {
			for (let i = 0; i < ref.data['Depth'].length; i++) {
				if (checkbox.active.indexOf(4)>-1) {
					if (depth <= ref.data['Depth'][i] && af <= ref.data['AF'][i] && ref.data['Syn'][i]=='synonymous SNV') {
						for (let b = 0; b < colnames.length; b++) {
							depth_sample.data[colnames[b]].push(ref.data[colnames[b]][i]);
						}
					}
				}
				else {
					if (depth <= ref.data['Depth'][i] && af <= ref.data['AF'][i] && ref.data['Syn'][i]=='synonymous SNV' && muts.includes(ref.data['Change'][i])) {
						for (let b = 0; b < colnames.length; b++) {
							depth_sample.data[colnames[b]].push(ref.data[colnames[b]][i]);
						}
					}
				}
			}
		}
		if (checkbox.active.indexOf(1)>-1) {
			for (let i = 0; i < ref.data['Depth'].length; i++) {
				if (checkbox.active.indexOf(4)>-1) {
					if (depth <= ref.data['Depth'][i] && af <= ref.data['AF'][i] && ref.data['Syn'][i]=='nonsynonymous SNV') {
						for (let b = 0; b < colnames.length; b++) {
							depth_sample.data[colnames[b]].push(ref.data[colnames[b]][i]);
						}
					}
				}
				else {
					if (depth <= ref.data['Depth'][i] && af <= ref.data['AF'][i] && ref.data['Syn'][i]=='nonsynonymous SNV' && muts.includes(ref.data['Change'][i])) {
						for (let b = 0; b < colnames.length; b++) {
							depth_sample.data[colnames[b]].push(ref.data[colnames[b]][i]);
						}
					}
				}
			}
		}
		if (checkbox.active.indexOf(2)>-1) {
			for (let i = 0; i < ref.data['Depth'].length; i++) {
				if (checkbox.active.indexOf(4)>-1) {
					if (depth <= ref.data['Depth'][i] && af <= ref.data['AF'][i] && (ref.data['Syn'][i]=='stopgain'||ref.data['Syn'][i]=='stoploss')) {
						for (let b = 0; b < colnames.length; b++) {
							depth_sample.data[colnames[b]].push(ref.data[colnames[b]][i]);
						}
					}
				}
				else {
					if (depth <= ref.data['Depth'][i] && af <= ref.data['AF'][i] && (ref.data['Syn'][i]=='stopgain'||ref.data['Syn'][i]=='stoploss') && muts.includes(ref.data['Change'][i])) {
						for (let b = 0; b < colnames.length; b++) {
							depth_sample.data[colnames[b]].push(ref.data[colnames[b]][i]);
						}
					}
				}
			}
		}
		if (checkbox.active.indexOf(3)>-1) {
			for (let i = 0; i < ref.data['Depth'].length; i++) {
				if (checkbox.active.indexOf(4)>-1) {
					if (depth <= ref.data['Depth'][i] && af <= ref.data['AF'][i] && (ref.data['Syn'][i]=='complex')) {
						for (let b = 0; b < colnames.length; b++) {
							depth_sample.data[colnames[b]].push(ref.data[colnames[b]][i]);
						}
					}
				}
				else {
					if (depth <= ref.data['Depth'][i] && af <= ref.data['AF'][i] && (ref.data['Syn'][i]=='complex') && muts.includes(ref.data['Change'][i])) {
						for (let b = 0; b < colnames.length; b++) {
							depth_sample.data[colnames[b]].push(ref.data[colnames[b]][i]);
						}
					}
				}
			}
		}
        depth_sample.change.emit();
    """)

# Second slider callback so that manual depth input overrides the slider.
def sliderCallback2(ref_source, source, slider, slider_af, syngroup, ose, muts):
		return CustomJS(args=dict(ref=ref_source, depth_sample=source, slider=slider, slider_af=slider_af, checkbox=syngroup, ose=ose, muts=unique_longitudinal_muts), code = """
			let depth = Number(ose.value);
			let af = slider_af.value;
			let colnames = Object.keys(ref.data);
			for (let a = 0; a < colnames.length; a++) {
				depth_sample.data[colnames[a]] = [];
			}
			if (checkbox.active.indexOf(0)>-1) {
				for (let i = 0; i < ref.data['Depth'].length; i++) {
					if (checkbox.active.indexOf(4)>-1) {
						if (depth <= ref.data['Depth'][i] && af <= ref.data['AF'][i] && ref.data['Syn'][i]=='synonymous SNV') {
							for (let b = 0; b < colnames.length; b++) {
								depth_sample.data[colnames[b]].push(ref.data[colnames[b]][i]);
							}
						}
					} 
					else {
						if (depth <= ref.data['Depth'][i] && af <= ref.data['AF'][i] && ref.data['Syn'][i]=='synonymous SNV' && muts.includes(ref.data['Mut'][i])) {
							for (let b = 0; b < colnames.length; b++) {
								depth_sample.data[colnames[b]].push(ref.data[colnames[b]][i]);
							}
						}
					}
				}
			}
			if (checkbox.active.indexOf(1)>-1) {
				for (let i = 0; i < ref.data['Depth'].length; i++) {
					if (checkbox.active.indexOf(4)>-1) {
						if (depth <= ref.data['Depth'][i] && af <= ref.data['AF'][i] && ref.data['Syn'][i]=='nonsynonymous SNV') {
							for (let b = 0; b < colnames.length; b++) {
								depth_sample.data[colnames[b]].push(ref.data[colnames[b]][i]);
							}
						}
					}
					else {
						if (depth <= ref.data['Depth'][i] && af <= ref.data['AF'][i] && ref.data['Syn'][i]=='nonsynonymous SNV' && muts.includes(ref.data['Mut'][i])) {
							for (let b = 0; b < colnames.length; b++) {
								depth_sample.data[colnames[b]].push(ref.data[colnames[b]][i]);
							}
						}
					}
				}
			}
			if (checkbox.active.indexOf(2)>-1) {
				for (let i = 0; i < ref.data['Depth'].length; i++) {
					if (checkbox.active.indexOf(4)>-1) {
						if (depth <= ref.data['Depth'][i] && af <= ref.data['AF'][i] && (ref.data['Syn'][i]=='stopgain'||ref.data['Syn'][i]=='stoploss')) {
							for (let b = 0; b < colnames.length; b++) {
								depth_sample.data[colnames[b]].push(ref.data[colnames[b]][i]);
							}
						}
					}
						else {
							if (depth <= ref.data['Depth'][i] && af <= ref.data['AF'][i] && (ref.data['Syn'][i]=='stopgain'||ref.data['Syn'][i]=='stoploss') && muts.includes(ref.data['Mut'][i])) {
							for (let b = 0; b < colnames.length; b++) {
								depth_sample.data[colnames[b]].push(ref.data[colnames[b]][i]);
							}
						}
					}
				}
			}
			if (checkbox.active.indexOf(3)>-1) {
				for (let i = 0; i < ref.data['Depth'].length; i++) {
					if (checkbox.active.indexOf(4)>-1) {
						if (depth <= ref.data['Depth'][i] && af <= ref.data['AF'][i] && (ref.data['Syn'][i]=='complex')) {
							for (let b = 0; b < colnames.length; b++) {
								depth_sample.data[colnames[b]].push(ref.data[colnames[b]][i]);
							}
						}
					}
						else {
							if (depth <= ref.data['Depth'][i] && af <= ref.data['AF'][i] && (ref.data['Syn'][i]=='complex') && muts.includes(ref.data['Mut'][i])) {
							for (let b = 0; b < colnames.length; b++) {
								depth_sample.data[colnames[b]].push(ref.data[colnames[b]][i]);
							}
						}
					}
				}
			}
            depth_sample.change.emit();
        """)

	
if __name__ == '__main__':
	parser = argparse.ArgumentParser(description='no description yet')
	parser.add_argument('-png', action='store_true')
	parser.add_argument('-nuc', action='store_true')
	parser.add_argument('-pdb', help='Provide a PDB acsession number to load into the NGL viewer')
	parser.add_argument('merged', help='internal call pointing to the merged.csv file created by the main lava script')
	parser.add_argument('proteins', help='Internal call pointing to the proteins.csv file created by the main lava script')
	parser.add_argument('reads', help='Internal call pointing to the reads.csv file created by the main lava script')
	parser.add_argument('dir', help='Dir created by main lava program')
	parser.add_argument('ptitle', help='Optional plot title specified by user.')
	parser.add_argument('-af', help="Provide a specific allele frequency to cut off.")
	
	try:
		args = parser.parse_args()
	except:
		parser.print_help()
		sys.exit(0)
	pdb_num = args.pdb 
	new_dir = args.dir

	# Reads data from lava output.
	merged = pd.read_csv(args.merged,index_col=False)
	proteins = pd.read_csv(args.proteins,index_col=False,header=None)
	reads = pd.read_csv(args.reads, index_col=False, names = ["Sample", "Total", "Mapped", "Percentage"])

	source = ColumnDataSource(merged)
	list_tabs = []
	list2_tabs = []
	list_plots = []
	list2_plots = []

	num_samples = merged.Sample.nunique()
	unique_samples = merged.Sample.unique()
	print(unique_samples)
	unique_samples = np.sort(merged.Sample.unique())
	num_Passages = merged['Passage'].max()
	protein_names = []

	user_af = -123
	if args.af:
		user_af = int(args.af)
	plot_title = args.ptitle.split('/')[-1]

	TOOLTIPS = [
		("Amino Acid Change", "@Change"),
		("Nucleotide Change", "@NucleotideChange"),
		("Allele Frequency", "@AF"+"%"),
		("Depth", "@Depth"),
	]
	FIRST = True
	

	# Create genome plots.
	# These graphs plot genome position on the x-axis (indicated by proteins), and allele frequency on the y-axis. Tabs allow
	# navigation between samples on the top. Mutations are color-coded by type (synonymous, nonsynonymous, stopgain/loss, or complex.)
	# To the side, genome coverage is plotted and read mapping information is given.
	# Depth and allele frequency cutoffs can be specified by sliders to the side.
	for sample_name, merged_Sample in merged.groupby('Sample', sort=False):
		sample = merged_Sample
		name = sample_name
		syn_factors = ['nonsynonymous SNV', 'synonymous SNV', 'complex', 'stopgain', 'stoploss']
		
		# Plot per base coverage for each sample as a subplot to the side.
		coverage = pd.read_csv(sample_name.strip() + '.genomecov', names=["sample", 'position', 'cov'], header=0, sep='\t')
		cov_sample = ColumnDataSource(coverage)
		cov_sample.data['position'].astype(float)
		cov_val_sample = ColumnDataSource(data=cov_sample.data)
		
		cov_graph = figure(plot_width=400, plot_height=200, title='Coverage')
		cov_graph.line(x='position', y='cov',source=cov_val_sample)
		
		# Initializes sample data.
		source_sample = ColumnDataSource(merged_Sample)
		source_sample.data['Position'].astype(float)
		depth_sample = ColumnDataSource(data=source_sample.data)

		# Creates a graph with x-axis being genome length (based on protein csv).
		## Took out active_scroll = "wheel_zoom" -RCS
		genome_plot = figure(plot_width=1600, plot_height=800, y_range=DataRange1d(bounds=(0,102), start=0,end=102),
			title=sample_name.split('/')[1], sizing_mode = 'scale_width',
			x_range=DataRange1d(bounds=(0, proteins.iloc[proteins.shape[0]-1,2]), start=0, end=proteins.iloc[proteins.shape[0]-1,2]))
		
		# Plots by nucleotide letter change.
		if(args.nuc):
			genome_plot.circle(x='Position', y=jitter('AF', width=2, range=genome_plot.y_range), size=15, alpha=0.6, hover_alpha=1, 
				legend = 'LetterChange', line_color='white', line_width=2, line_alpha=1,
				fill_color=factor_cmap('LetterChange', palette=color_palette, factors=merged.LetterChange.unique()), 
				hover_color=factor_cmap('LetterChange', palette=color_palette, factors=merged.LetterChange.unique()),
				source=depth_sample, hover_line_color='white')
		# Plots by amino acid change type.
		else:
			genome_plot.circle(x='Position', y='AF', size=15, alpha=0.6, hover_alpha=1, 
				legend = 'Syn', line_color='white', line_width=2, line_alpha=1,
				fill_color=factor_cmap('Syn', palette=['firebrick', 'cornflowerblue', 'green', 'purple', 'yellow'], factors=syn_factors), 
				hover_color=factor_cmap('Syn', palette=['firebrick', 'cornflowerblue', 'green', 'purple', 'yellow'], factors=syn_factors),
				source=depth_sample, hover_line_color='white')
		
		# Sets up visualization and hover tool.
		genome_plot.add_tools(HoverTool(tooltips=TOOLTIPS))
		genome_plot.xgrid.grid_line_alpha = 0
		configurePlot(genome_plot)
		protein_names = protein_annotation(FIRST)
		FIRST = False
		genome_plot.xaxis.axis_label = "Protein"

		# Creates button that allows reset of plot to original state.
		reset_button = Button(label="Reset Plot")
		reset_button.js_on_click(CustomJS(args=dict(g=genome_plot), code="""
			g.reset.emit()
		"""))

		# Creates text input button for user manual input of depth.
		ose = TextInput(title='Manually input depth:')
		
		# Creates checkboxes to show different types of mutations.
		syngroup = CheckboxGroup(labels=["Show synonymous mutations", "Show nonsynonymous mutations", 
			"Show stopgains and stoplosses", "Show complex mutations", "Show mutations without longitudinal data"], active=[0,1,2,3,4])

		# Grabs the mutations that occur multiple times across samples.
		longitudinal_muts = merged_Sample[merged_Sample.duplicated('Change', keep=False)]
		unique_longitudinal_muts = longitudinal_muts.Change.unique()
		
		# Initializes and filters data based on slider values.
		slider = Slider(start=5, end=merged['Depth'].max(), step=1, value=5, title='Depth Cutoff')
		slider_af = Slider(start=5, end=100, step=1, value=5, title='Allele Frequency Cutoff')
		slider_af.js_on_change('value', sliderCallback(source_sample, depth_sample, slider, slider_af,syngroup, unique_longitudinal_muts))
		slider.js_on_change('value', sliderCallback(source_sample, depth_sample, slider, slider_af, syngroup, unique_longitudinal_muts))
		syngroup.js_on_change('active', sliderCallback(source_sample, depth_sample, slider, slider_af, syngroup, unique_longitudinal_muts))
		ose.js_on_change('value', sliderCallback2(source_sample, depth_sample, slider, slider_af, syngroup, ose, unique_longitudinal_muts))

		# When mousing over Bokeh plot, allele frequency updated to user input.
		if(user_af!= -123):
			slider_af.value = user_af
			## g.js_on_event(events.PlotEvent, sliderCallback(source_sample, depth_sample, slider, slider_af, syngroup))
			genome_plot.js_on_event(events.MouseEnter, sliderCallback(source_sample, depth_sample, slider, slider_af, syngroup, unique_longitudinal_muts))

		# Creates labels with read information
		reads_info = (reads.loc[reads['Sample'] == name.strip()])
		div=Div(text="""<font size="2" color="gray"><b>Total reads: </b>"""+str(reads_info.iloc[0]["Total"])+
			"""<br><b>Total reads mapped: </b>"""+str(reads_info.iloc[0]["Mapped"])+"""<br><b>Percentage of reads mapped: </b>
			"""+str(reads_info.iloc[0]["Percentage"])+"""</font>""", width=300, height=100)
		
		# Plots layout of all components.
		genome_plot = layout(row([genome_plot, column([Div(text="""""", width=300, height=220),cov_graph,ose, slider, slider_af, syngroup, widgetbox(div),reset_button])]))
    	
		# Creates both tabs and different plots for each sample.
		tab = Panel(child=genome_plot, title=name.split('/')[-1])
		list_tabs.append(tab)
		list_plots.append(genome_plot)
	
	tabs_genomes = Tabs(tabs=list_tabs)
	plots_genomes = (column(list_plots))
	
	total_num_mutations = 0

	# Sorts data by protein location.
	merged.Protein = merged.Protein.astype("category")
	merged.Protein.cat.set_categories(protein_names, inplace=True)
	merged.sort_values(["Protein"])

	# Creates protein plots.
	# These graphs plot sample # (based on metadata) on x-axis, and alelle frequency on the y-axis. Tabs allow
	# navigation between different proteins on the top, organized by genome location.
	# To the side, genome coverage is plotted. Depth and allele frequency cutoffs can be specified.
	# Lines connecting mutations across samples show up when the mutations are hovered over,
	# allowing visualization of evolution of mutations across time.
	
	
# Outputs files into html or png files as requested.
	if(args.nuc):
		output_file(new_dir + "/" + "nucleotide_changes.html", title=plot_title)
		show(tabs_genomes)
	else:
		if(args.png):
			export_png(plots_proteins, filename="Protein_Plots.png")
			export_png(plots_genomes, filename="Genome_Plots.png")
		else:
			# Saves output both as standalone HTML file and as a javascript element and a script tag.
			output_file(new_dir + "/" + new_dir + "_plots.html", title=plot_title)
			print('Opening output file genome_protein_plots.html...\nGraphs_and_viewer.html includes the protein viewer.')
#			output_file(new_dir + "/" + new_dir + "_plots.html", title=plot_title)
# 			## subprocess.call('cp ngls_test.html ' + new_dir + '/', shell=True)
			save(column(tabs_genomes))
			# Automatically opens output file, otherwise prints error message.
			try:
				show(column(tabs_genomes))
			except:
				print('Automatic opening of output files has failed - however generation worked. Check out your output at the above paths.')
