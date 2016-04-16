is_valid = (x) -> (x?) and (x == x)

get_inlier_range = (x) ->
	x = (p for p in x when is_valid p)
	[q1, q3] = science.stats.quantiles x, [0.25, 0.75]
	iqr = q3 - q1
	return [q1 - 3.5*iqr, q3 + 3.5*iqr]

get_outlier_idx = (xs, rng) ->
	outliers = {}
	for x, xi in xs
		continue if x != x or x > rng[0] and x < rng[1]
		outliers[xi] = true
	return outliers

clamp_to_range = (xs, rng) ->
	(Math.min(Math.max(x, rng[0]), rng[1]) for x in xs)

@income_vote_scatter = ($el, data, opts) ->
	x_field = opts.x ? 'millenial_share'
	y_field = opts.y ? 'vote_share'
	
	x = data[x_field].map parseFloat
	y = data[y_field].map parseFloat

	if opts.show_outliers == "true"
		xrng = [-Infinity, Infinity]
		yrng = [-Infinity, Infinity]
	else
		xrng = get_inlier_range x
		yrng = get_inlier_range y


	
	outlier_idx = get_outlier_idx x, xrng
	outlier_idx = _.extend outlier_idx, get_outlier_idx y, yrng
	n_outliers = (k for k of outlier_idx).length
	if n_outliers == x.length
		outlier_idx = {}

	outliers = {}
	for name of data
		col_in = []
		col_out = []
		for i, v of data[name]
			if i of outlier_idx
				col_out.push v
			else
				col_in.push v
		data[name] = col_in
		outliers[name] = col_out
	
	x = data[x_field].map parseFloat
	y = data[y_field].map parseFloat
	xy = _.zip x, y
	xy_valid = (p for p in xy when is_valid(p[0]) and is_valid(p[1]))
	
	y_out = clamp_to_range(outliers[y_field].map(parseFloat), yrng)
	xy_out = _.zip(
		clamp_to_range(outliers[x_field].map(parseFloat), xrng),
		y_out
		)

	xy_sorted = _.sortBy xy_valid, (xy) -> xy[0]
	[x_sort_valid, y_sort_valid] = _.zip xy_sorted...

	all_y = y_sort_valid.concat(y_out)
	y_disp_rng = [Math.min(all_y...), Math.max(all_y...)]

	

	loess = science.stats.loess().bandwidth(0.8)
	ys = loess(x_sort_valid, y_sort_valid)

	scatter =
		data: xy
		points:
			show: true
			fillColor: "rgb(0, 33, 37)"
			radius: 3
		color: "rgb(0, 33, 37)"

	outlier_scat =
		data: xy_out
		points:
			show: true
			fillColor: "#cccccc"
			radius: 3
		color: "#cccccc"
	
	if $el.width() < 578
		scatter.points.radius = 3
	
	line =
		data: _.zip x_sort_valid, ys
		points:
			show: false
		lines:
			show: true
		color: "rgb(0, 180, 200)"
	
	floatOrUnd = (v) ->
		v = parseFloat v
		if v != v
			return undefined
		return v
	plotopts =
		series:
			shadowSize: 0
		xaxis:
			axisLabel: opts.axis_labels[x_field] ? x_field
			tickFormatter: (v) -> opts.value_formatter x_field, v
			ticks: 4
		yaxis:
			ticks: 4
			axisLabel: opts.axis_labels[y_field] ? y_field
			tickFormatter: (v) -> opts.value_formatter y_field, v
			min: y_disp_rng[0]
			max: y_disp_rng[1]
		grid:
			hoverable: true
			borderWidth:
				left: 1
				right: 1
				top: 1
				bottom: 1
		#selection:
		#	mode: "xy"
	
	plot = $.plot $el, [line, scatter, outlier_scat], plotopts
	
	$el.powerTip
		smartPlacement: true
		followMouse: true
		closeDelay: 0
		fadeOutTime: 0
		fadeInTime: 0
	
	prev_item = null
	handle_tooltip = (ev, pos, item) ->
		if not item or item.seriesIndex == 0
			plot.unhighlight()
			$el.powerTip "hide"
			$.powerTip.hide()
			return
		if item == prev_item
			return
		if item != prev_item
			# Must hide in between for the
			# data to be refreshed
			$el.powerTip "hide"
			$.powerTip.hide()
		prev_item = item
		
		dataset = [data, outliers][item.seriesIndex-1]

		tooltip = $ """<div class="tooltip"></div>"""
		tooltip.append $ """<div>#{dataset[opts.tt_title ? 'place_name'][item.dataIndex]}</div>"""
		dl = $("""<dl></dl>""").appendTo tooltip
		fields = [x_field, y_field].concat(opts.fields ? [])
		for field in fields
			label = opts.tooltip_labels[field] ? field
			dl.append $ "<dt>#{label}</dt>"
			value = dataset[field][item.dataIndex]
			dl.append $ "<dd>#{opts.value_formatter field, value}</dd>"
		$el.data "powertipjq", tooltip

		$el.powerTip "show"

	$el.unbind "plothover"
	$el.bind "plothover", handle_tooltip
	$el.unbind "plotclick"
	$el.bind "plotclick", handle_tooltip
	
	if opts.csv
		open_rawdata = $("<a href='#' style='position: absolute: top: 0; margin-right: 80px;margin-top: -20px; width: 100px; float: right;'>Raakadata</a>").appendTo $el
		open_rawdata.click (ev) ->
			ev.preventDefault()
			w = window.open('', '', 'width=400,height=400,resizeable,scrollbars')
			w.document.charset = 'utf-8'
			w.document.write('<pre>')
			w.document.write("#{x_field};#{y_field};#{opts.tt_title}\n")
			for [x, y], i in xy
				w.document.write("#{x};#{y};#{data[opts.tt_title][i]}\n")
			w.document.write('</pre>')
			w.document.close()
			return false
		
		open_rawdata = $("<a href='#' style='position: absolute: top: 0; right: 0;margin-top: -20px; width: 100px; float: right;'>Sovitus</a>").appendTo $el
		open_rawdata.click (ev) ->
			ev.preventDefault()
			w = window.open('', '', 'width=400,height=400,resizeable,scrollbars')
			w.document.charset = 'utf-8'
			w.document.write('<pre>')
			w.document.write("#{x_field};#{y_field}_fit\n")
			for [x, y], i in _.zip x, ys
				w.document.write("#{x};#{y}\n")
			w.document.write('</pre>')
			w.document.close()
			return false
	return -> plot.shutdown()
