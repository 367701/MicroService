function Rating(data){
  this.id = ko.observable(data.id);
  this.rating = ko.observable(data.rating);
  this.comment = ko.observable(data.comment);
  this.product_id = ko.observable(data.product_id);
}

function Product(data) {
  var averageRating = 0;

  $.getJSON('/api/v1/ratings/' + data.id, function(ratingModels) {
    $.each(ratingModels, function(index, value) {
      var totalRating = 0;
      for(var i = 0; i < value.length; i++){
        var test = value[i].toString().split("'").join("\"");
        var obj = JSON.parse(test);
        totalRating += obj.rating;
        console.log(totalRating);
      }
      averageRating = (totalRating / value.length);
    });
  });

  this.id = ko.observable(data.id);
  this.name = ko.observable(data.name);
  this.category = ko.observable(data.category);
  this.rrp = ko.observable("£" + data.rrp);
  this.description = ko.observable(data.description);
  this.weight = ko.observable(data.weight + "g");
  this.image = ko.observable(data.image);

  this.rating = ko.observable(averageRating);
  this.reviewLink = ko.observable("./review/" + data.id);
}



function ProductListViewModel() {
    var self = this;
    self.product_list = ko.observableArray([]);
    self.name = ko.observable();
    self.category = ko.observable();
    self.rrp = ko.observable();
    self.description = ko.observable();
    self.weight = ko.observable();
    self.image = ko.observable();
    self.rating = ko.observable();

    self.addProduct = function() {
    	self.save();
      self.name("");
    	self.category("");
    	self.rrp("");
      self.description("");
      self.weight("");
      self.image("");
      self.rating("");
    };

    $.getJSON('/api/v1/products', function(productModels) {
    	var t = $.map(productModels.products_list, function(item) {
    	    return new Product(item);
    	});
    	self.product_list(t);
    });


}

ko.applyBindings(new ProductListViewModel());
