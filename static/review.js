function Rating(data){
  this.id = ko.observable(data.id);
  this.rating = ko.observable(data.rating);
  this.comment = ko.observable(data.comment);
  this.product_id = ko.observable(data.product_id);
  this.username = ko.observable(data.username);
}

function RatingListViewModel() {
    var self = this;

    self.rating = ko.observable();
    self.comment= ko.observable();
    self.product_id= ko.observable();
    self.username = ko.observable();

    self.addRating = function() {
	self.save();
  self.rating("");
	self.comment("");
	self.product_id("");
  self.username("");
    };

    self.save = function() {
	return $.ajax({
	    url: '/api/v1/ratings',
	    contentType: 'application/json',
	    type: 'POST',
	    data: JSON.stringify({
		'rating': document.getElementById("rating").value,
		'comment': self.comment(),
    'product_id': document.getElementById("product_id").value,
    'username': self.username()
	    }),
	    success: function(data) {
          alert("success");
		      window.location.href = '/products';
	    },
	    error: function() {
		return console.log("Failed");
	    }
	});
    };
}

ko.applyBindings(new RatingListViewModel());
