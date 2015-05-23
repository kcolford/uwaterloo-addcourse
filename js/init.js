// Configuration for the addcourse page.

jQuery(document).ready(function ($) {
  $("body > div.section").changeElementType("section");

  $("section#credits").changeElementType("footer");

  $("section > *").each(function() {
    $(this).replaceWith("<div class=\"row\">" + $(this).text() + "</div>");
  });

});
