/* eslint-env browser, jquery */

/* {{{ Development */

const DEVELOPMENT = true;

DebugObjS = function DebugObjS(o) {
  let ss = o + ': ';
  for (const id in o) {
    ss += id;
    ss += ' ';
  }
  alert(ss);
};

LOG = function LOG() {
  let s = '';

  for (let i = 0; i < arguments.length; i++) {
    s += arguments[i] + ' ';
  }
  if (arguments.length) {
    s += '<br/>';
  }

  let LOG = jQuery('#LOG');

  if (!LOG.length) {
    const xTop = 0;
    // if ( jQuery('#DIM').length ) { xTop += 30; }
    jQuery('body').append('<div id="LOG"></div>');
    LOG = jQuery('#LOG');
    LOG.css({
      // display: 'block',
      overflow: 'hidden',
      'line-height': '200%',
      'z-index': '9000',
      width: '100%',
      position: 'fixed',
      top: xTop + 'px',
      'font-family': 'Lucida Console, monospace',
      'font-size': '8pt',
      'white-space': 'pre',
      border: '1px solid rgba(0,0,0,.25)',
      background: 'rgba(0,0,0,.75)',
      color: 'rgba(200,200,200,.75)',
      padding: '5px',
      'padding-left': '10px',
      margin: '10px auto',
    });
    LOG.click(function () {
      jQuery(this).hide(200).html('');
      return false;
    });
  }

  LOG.html(LOG.html() + s);
  if (arguments.length && LOG.is(':hidden')) {
    LOG.show();
  }
};

function DIM() {
  if (typeof DEVELOPMENT == 'undefined' || !DEVELOPMENT) {
    return;
  }
  let DIM = jQuery('#DIM');
  // Create new node if absent...
  if (!DIM.length) {
    jQuery('body').append(
      '<div id="DIM" style="display: none;" title="Dev info toolbar: Click to hide"></div>',
    );
    DIM = jQuery('#DIM');
    DIM.click(function () {
      jQuery(this).hide(200).html('');
      return false;
    });
    // Show with a delay...
    setTimeout(DIM.show.bind(DIM, 200), 1000);
  }
  // Update content (unconditionally)...
  DIM.html(
    jQuery(document).width() +
      '<span>x</span>' +
      jQuery(document).height() +
      '<span>(</span>' +
      jQuery(window).height() +
      '<span>)</span>',
  );
}

function DevelopmentWindowUpdate() {
  DIM();
}

jQuery(window).resize(function () {
  DevelopmentWindowUpdate();
});
jQuery(document).ready(function () {
  DevelopmentWindowUpdate();
});

/* Development }}} */
