/* -*- tab-width: 2; indent-tabs-mode: nil; c-basic-offset: 2; js-indent-level: 2; -*- */
define(['underscore', 'backbone'], function(_, Backbone) {
  'use strict';

  var Annotation =  Backbone.Model.extend({
    defaults: {
      uuid: null,
      label: "",
      type: "",
      highlighted: false,
      content: "",
      mapping: {}
    },
    highlight: function() {
      var highlighted = !this.get("highlighted");
      this.set({ highlighted: highlighted });
    },
    select: function() {
      this.trigger("select", this.get("uuid"));
    }
  });

  return Annotation;


});
