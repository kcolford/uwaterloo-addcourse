// Configuration for the addcourse page.

jQuery(document).ready(function ($) {
  $("body > div.section").changeElementType("section");

  $("section#credits").changeElementType("footer");

  $("body > :not(section)").wrapAll("<header></header>");

  $("section").wrapInner("<div class='row'></div>");

});
