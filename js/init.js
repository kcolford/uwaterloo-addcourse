// Configuration for the addcourse page.

jQuery(document).ready(function ($) {
  $("body > div.section").changeElementType("section");
  $("body > :not(section)").wrapAll("<header></header>");
  $("section").wrapInner("<div class='row'></div>");
  $("section#credits").changeElementType("footer");
});
