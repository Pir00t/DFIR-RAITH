# Author: Steven Folek | @Pir00t
# Version: 1.0

from ipyaggrid import Grid

def df2grid(df, pageSize=10, wrapText=False):
	"""Take dataframe and return interactive object to be rendered in browser
	
	Args:
		df: dataframe to render
		pageSize: default=10 - number of results to show per page
		wrapText: default=False - Set to True for text wrapping in columns

	Returns:
		grid: interactive object
	"""
	
	# adapted from https://github.com/ds4n6/ds4n6_lib/blob/ac26cbf5f73278195c6b35ea0d084a2c9d3eaad6/src/ds4n6_lib/gui.py
	column_defs = [{'headerName': df.index.name, 'field': df.index.name}]
	column_defs +=  [{'headerName': c, 'field': c, 'checkboxSelection': True, 'autoHeight': True, 'wrapText': wrapText} for c in df.columns]
	
	gridOptions = {
			'columnDefs': column_defs,
			'defaultColDef': {'sortable': True, 'filter': True, 'resizable': True, 'floatingFilter': True},
			'animateRows': True,
			'enableRangeSelection': True,
			'enableColResize': True,
			'rowSelection': 'multiple',
			'enableFilter': True,
			'enableSorting': True,
			'pagination':True,
			'paginationPageSize': pageSize
		}
	grid = Grid(
		grid_data=df,
		grid_options=gridOptions, 
		quick_filter=True,
		columns_fit="auto",
		export_csv=True,
		export_mode='auto',
		export_to_df=True,
		keep_multiindex=False,
		theme="ag-theme-balham-dark",
		index=True 
	)
	return grid