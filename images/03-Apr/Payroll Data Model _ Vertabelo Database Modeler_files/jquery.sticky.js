/* http://keith-wood.name/sticky.html
   Sticky element for jQuery v1.0.0.
   Written by Keith Wood (kwood{at}iinet.com.au) November 2014.
   Available under the MIT (http://keith-wood.name/licence.html) license. 
   Please attribute the author if you use it. */

(function($) { // Hide scope, no $ conflict

	var pluginName = 'sticky';
	
	var uid = 1;

	/** Create the sticky element plugin.
		<p>Sets an element to remain at the top of the page during scrolling.</p>
		<p>Expects HTML like:</p>
		<pre>&lt;div id="content">...&lt;/div>
&lt;div id="aside">
	&lt;div id="sticky">...&lt;/div>
&lt;/div></pre>
		<p>Provide inline configuration like:</p>
		<pre>&lt;div data-sticky="name: 'value'">...&lt;/div></pre>
	 	@module Sticky
		@augments JQPlugin
		@example $(selector).sticky()
 $(selector).sticky({offset: 20}) */
	$.JQPlugin.createPlugin({
	
		/** The name of the plugin. */
		name: pluginName,

		/** Sticky scrolled change callback.
			Triggered when the window is scrolled or resized.
			@callback stickyScrolled
			@param status {string} The current positioning of the element: top|float|bottom. */
			
		/** Default settings for the plugin.
			@property [boundedBy='#content'] {string|Element|jQuery} The selector, DOM element, or jQuery collection for
					the element that defines the top and bottom boundaries within which the sticky element stays.
			@property [marginTop=0] {number} Any additional space reserved at the page top (pixels).
			@property [scrolled=null] {stickyScrolled} A callback when the page is scrolled. */
		defaultOptions: {
			boundedBy: '#content',
			marginTop: 0,
			scrolled: null
		},

		_instSettings: function(elem, options) {
			var parent = elem.parent();
			var position = parent.css('position');
			elem.parent().css('position', 'relative');
			var marker = $('<div></div>').insertBefore(elem);
			return {boundedBy: $(options.boundedBy), parent: parent, position: position, marker: marker,
				lastPosition: 'static', lastTop: 0, uid: uid++};
		},
		
		_optionsChanged: function(elem, inst, options) {
			if (inst.boundedBy.length) {
				var namespace = '.' + this.name + inst.uid;
				$(window).off(namespace).
					on('scroll' + namespace + ' resize' + namespace, {inst: inst}, this._windowScroll).
					trigger('scroll', {data: {inst: inst}});
			}
		},

		/** Update element position when the page scrolls.
			@param e {Event} The triggering event. */
		_windowScroll: function(e) {
			var inst = e.data.inst;
			var scrollPosition = $(window).scrollTop() + inst.options.marginTop;
			var contentBottom = inst.boundedBy.outerHeight() + inst.boundedBy.offset().top - inst.options.marginTop;
			var parentTop = inst.parent.offset().top;
			var stickyElementHeight = inst.elem.outerHeight();
			var position = 'static';
			var top = 0;
			var status = 'top';
			if ((scrollPosition + stickyElementHeight) > contentBottom) {
				position = 'absolute';
				top = contentBottom - stickyElementHeight - parentTop;
				status = 'bottom';
			} else if (scrollPosition >= inst.marker.offset().top) {
				position = 'absolute';
				top = scrollPosition - parentTop;
				status = 'float';
			}
			if (inst.lastPosition !== position || inst.lastTop !== top) {
				inst.elem.css({position: position, top: top});
				inst.lastPosition = position;
				inst.lastTop = top;
				if ($.isFunction(inst.options.scrolled)) {
					inst.options.scrolled.call(inst.elem[0], [status]);
				}
			}
		},

		_preDestroy: function(elem, inst) {
			elem.css({position: 'static', top: 0}).parent().css({position: inst.position});
			inst.marker.remove();
			$(window).off('.' + this.name + inst.uid);
		}
	});

})(jQuery);
