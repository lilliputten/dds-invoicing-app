/*{{{ Development */

DEVELOPMENT = true;

function DebugObjS (o)/*{{{*/
{
	var ss = o+': ';
	for ( id in o ) {
		ss += id;
		ss += ' ';
	}
	alert(ss);
}/*}}}*/

function LOG ()/*{{{*/
{
	var s = '';

	for (var i=0; i<arguments.length; i++) {
		s += arguments[i] + ' ';
	}
	if ( arguments.length ) {
		s += '<br/>';
	}

	var LOG = jQuery('#LOG');

	if ( !LOG.length ) {
		var xTop = 0;
		// if ( jQuery('#DIM').length ) { xTop += 30; }
		jQuery('body').append('<div id="LOG"></div>');
		LOG = jQuery('#LOG');
		LOG.css( {
			'overflow': 'hidden',
			'line-height': '200%',
			'z-index': '9000',
			'width': '100%',
			'position': 'fixed',
			'top': xTop+'px',
			'font-family': 'Lucida Console, monospace',
			'font-size': '8pt',
			'white-space': 'pre',
			'border': '1px solid rgba(0,0,0,.25)',
			'background': 'rgba(0,0,0,.75)',
			'color': 'rgba(200,200,200,.75)',
			'padding': '5px',
			'padding-left': '10px',
			'margin': '10px auto',
		});
		LOG.click( function () { jQuery(this).hide(200).html(''); return false; } );
	}

	LOG.html(LOG.html()+s);
	if ( arguments.length && LOG.is(':hidden') ) {
		LOG.show();
	}

}/*}}}*/

function DIM ()/*{{{*/
{
	if ( typeof(DEVELOPMENT)=='undefined' || !DEVELOPMENT ) { return; }
	var DIM = jQuery('#DIM');
	if ( !DIM.length ) {
		jQuery('body').append('<div id="DIM"></div>');
		DIM = jQuery('#DIM');
		DIM.click( function () { jQuery(this).hide(200).html(''); return false; } );
		DIM.show(200);
	}
	DIM.html( jQuery(document).width()+'<span>x</span>'+jQuery(document).height()+'<span>(</span>'+jQuery(window).height()+'<span>)</span>' );
}/*}}}*/

function DevelopmentWindowUpdate ()/*{{{*/
{
	DIM();
}/*}}}*/

jQuery(window).resize(function()/*{{{*/
{

	DevelopmentWindowUpdate();

});/*}}}*/
jQuery(document).ready(function()/*{{{*/
{

	DevelopmentWindowUpdate();

	// jQuery('.demo-label').mouseover(DemoLabelOver);
	// jQuery('.demo-label').mouseout(DemoLabelOut);

});/*}}}*/

/* Development }}}*/
