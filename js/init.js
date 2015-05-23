// Configuration for the addcourse page.

jQuery(document).ready(function ($) {
  $("body > div.section").changeElementType("section");

  $("section#credits").changeElementType("footer");

  $("section").wrapInner("<div class='row'></div>");

});
