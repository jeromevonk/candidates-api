function CandidatesViewModel() {
    var self = this;
    self.candidatesURI = '../candidates/api/v2.0/candidates';
    self.username = "user";
    self.password = "123";
    self.candidates_array = ko.observableArray();

    self.ajax = function(uri, method, data) {
        var request = {
            url: uri,
            type: method,
            contentType: "application/json",
            accepts: "application/json",
            cache: false,
            dataType: 'json',
            data: JSON.stringify(data),
            beforeSend: function(xhr) {
                xhr.setRequestHeader("Authorization",
                    "Basic " + btoa(self.username + ":" + self.password));
            },
            error: function(jqXHR) {
                console.log("ajax error " + jqXHR.status);
                <!-- alert("Error!") -->
            }
        };
        return $.ajax(request);
    }

    self.ajax_send_batch = function(data) {
        var request = {
            url: '../candidates/api/v2.0/candidates/batch',
            data: data,
            accepts: "application/json",
            processData: false,
            contentType: false,
            type: 'POST',
            error: function(jqXHR) {
                console.log("ajax error " + jqXHR.status);
                alert("Error! Please check your zip file")
            }
        };
        return $.ajax(request);
    }

    self.updateCandidate = function(candidate, newCandidate) {
        var i = self.candidates_array.indexOf(candidate);
        self.candidates_array()[i].id(newCandidate.id);
        self.candidates_array()[i].name(newCandidate.name);
        self.candidates_array()[i].gender(newCandidate.gender);
        self.candidates_array()[i].email(newCandidate.email);
        self.candidates_array()[i].phone(newCandidate.phone);
        self.candidates_array()[i].address(newCandidate.address);
        self.candidates_array()[i].birthdate(newCandidate.birthdate);
        self.candidates_array()[i].latitude(newCandidate.latitude);
        self.candidates_array()[i].longitude(newCandidate.longitude);
        self.candidates_array()[i].education(newCandidate.education);
        self.candidates_array()[i].experience(newCandidate.experience);
        self.candidates_array()[i].tags(newCandidate.tags);
        self.candidates_array()[i].picture(newCandidate.picture);
    }

    self.beginAdd = function() {
        $('#add').modal('show');
    }
    self.add = function(task) {
        self.ajax(self.candidatesURI, 'POST', task).done(function(data) {
            self.candidates_array.push({
                id: ko.observable(data.inserted.id),
                name: ko.observable(data.inserted.name),
                gender: ko.observable(data.inserted.gender),
                email: ko.observable(data.inserted.email),
                phone: ko.observable(data.inserted.phone),
                address: ko.observable(data.inserted.address),
                birthdate: ko.observable(data.inserted.birthdate),
                latitude: ko.observable(data.inserted.latitude),
                longitude: ko.observable(data.inserted.longitude),
                education: ko.observable(data.inserted.education),
                experience: ko.observable(data.inserted.experience),
                tags: ko.observable(data.inserted.tags),
                picture: ko.observable(data.inserted.picture),

            });
        });
    }
    self.batch_insert = function(zipfile) {
        formdata = new FormData();
        formdata.append('zipfile', zipfile)
        self.ajax_send_batch(formdata).done(function(data) {
            alert('Added: ' + data.added + '\n' + 'Invalid: ' + data.invalid + '\n' + 'Updated: ' + data.updated + '\n');
            location.reload();
        });
    }
    self.beginEdit = function(candidate) {
        editCandidateViewModel.setCandidate(candidate);
        $('#edit').modal('show');
    }
    self.edit = function(candidate, data) {
        self.ajax(self.candidatesURI + '/' + candidate.id(), 'PUT', data).done(function(res) {
            self.updateCandidate(candidate, res.updated);
        });
    }
    self.remove = function(candidate) {
        self.ajax(self.candidatesURI + '/' + candidate.id(), 'DELETE').done(function() {
            self.candidates_array.remove(candidate);
        });
    }

    self.deleteAll = function() {
        self.ajax(self.candidatesURI, 'DELETE').done(function() {
            self.candidates_array.removeAll();
        });
    }

    self.ajax(self.candidatesURI, 'GET').done(function(data) {
        for (var i = 0; i < data.candidates.length; i++) {
            self.candidates_array.push({
                id: ko.observable(data.candidates[i].id),
                name: ko.observable(data.candidates[i].name),
                gender: ko.observable(data.candidates[i].gender),
                email: ko.observable(data.candidates[i].email),
                phone: ko.observable(data.candidates[i].phone),
                address: ko.observable(data.candidates[i].address),
                birthdate: ko.observable(data.candidates[i].birthdate),
                latitude: ko.observable(data.candidates[i].latitude),
                longitude: ko.observable(data.candidates[i].longitude),
                picture: ko.observable(data.candidates[i].picture),
                education: ko.observableArray(data.candidates[i].education),
                experience: ko.observableArray(data.candidates[i].experience),
                tags: ko.observableArray(data.candidates[i].tags),
            });
        }

    });
}

function AddCandidateViewModel() {
    var self = this;

    self.name = ko.observable("Some dude");
    self.gender = ko.observable("1");
    self.email = ko.observable("fake@fake.com");
    self.phone = ko.observable("11997511245");
    self.address = ko.observable("Rua dos quatro cantos do mundo");
    self.birthdate = ko.observable("18/02/1975");
    self.latitude = ko.observable("0.01");
    self.longitude = ko.observable("12.345");
    self.picture = "";
    self.tags = ko.observable("dude, man");
    self.company = ko.observable("LTDA");
    self.job_title = ko.observable("Owner");
    self.job_start = ko.observable("01/01/2015");
    self.job_end = ko.observable("01/01/2016");
    self.job_desc = ko.observable("Easy");
    self.institution = ko.observable("UVU");
    self.degree = ko.observable("Something");
    self.ed_start = ko.observable("01/01/2007");
    self.ed_end = ko.observable("01/01/2011");
    self.ed_desc = ko.observable("Hard");

    self.uploadImage = function(file) {
        /* Is the file an image? */
        if (!file || !file.type.match(/image.*/)) return;

        if (file.size > 100 * 1024) {
            alert("Sorry, that image is (for now) too big for this poor front-end app! Try smaller than 100KB")
            return
        }

        var reader = new FileReader();
        reader.addEventListener("load", function() {
            self.picture = reader.result.split(',')[1];
        }, false);
        reader.readAsDataURL(file);
    };

    self.addCandidate = function() {
        $('#add').modal('hide');

        to_add = {
            name: self.name(),
            gender: parseInt(self.gender(), 10),
            email: self.email(),
            phone: self.phone(),
            address: self.address(),
            birthdate: self.birthdate(),
            latitude: parseFloat(self.latitude(), 10),
            longitude: parseFloat(self.longitude(), 10),
            picture: self.picture,
            tags: [self.tags()],
        }

        <!-- Do we have education data? -->
        if (self.institution() == "" && self.degree() == "" && self.ed_start() == "" && self.ed_end() == "" && self.ed_desc() == "") {
            to_add['education'] = []
        } else {
            _education = {
                'institution': self.institution(),
                'degree': self.degree(),
                'date_start': self.ed_start(),
                'date_end': self.ed_end(),
                'description': self.ed_desc()
            };

            to_add['education'] = [_education];
        }

        <!-- Do we have experience data? -->
        if (self.company() == "" && self.job_title() == "" && self.job_start() == "" && self.job_end() == "" && self.job_desc() == "") {
            to_add['experience'] = []
        } else {
            _experience = {
                'company': self.company(),
                'job_title': self.job_title(),
                'date_start': self.job_start(),
                'date_end': self.job_end(),
                'description': self.job_desc()
            };

            to_add['experience'] = [_experience];
        }

        candidatesViewModel.add(to_add);

        <!-- Reset -->
        self.name("");
        self.gender("");
        self.email("");
        self.phone("");
        self.address("");
        self.birthdate("");
        self.latitude("");
        self.longitude("");
        self.picture = "";
        self.tags("");

    }
}

function EditCandidateViewModel() {
    var self = this;
    self.name = ko.observable();
    self.gender = ko.observable();
    self.email = ko.observable();
    self.phone = ko.observable();
    self.address = ko.observable();
    self.birthdate = ko.observable();
    self.latitude = ko.observable();
    self.longitude = ko.observable();
    self.picture = "";
    self.tags = ko.observable();
    self.company = ko.observable();
    self.job_title = ko.observable();
    self.job_start = ko.observable();
    self.job_end = ko.observable();
    self.job_desc = ko.observable();
    self.institution = ko.observable();
    self.degree = ko.observable();
    self.ed_start = ko.observable();
    self.ed_end = ko.observable();
    self.ed_desc = ko.observable();

    self.uploadImage = function(file) {
        /* Is the file an image? */
        if (!file || !file.type.match(/image.*/)) return;

        if (file.size > 100 * 1024) {
            alert("Sorry, that image is (for now) too big for this poor front-end app! Try smaller than 100KB")
            return
        }

        var reader = new FileReader();
        reader.addEventListener("load", function() {
            self.picture = reader.result.split(',')[1];
        }, false);
        reader.readAsDataURL(file);
    };

    self.setCandidate = function(candidate) {
        self.candidate = candidate;
        self.name(candidate.name());
        self.gender(candidate.gender());
        self.email(candidate.email());
        self.phone(candidate.phone());
        self.address(candidate.address());
        self.birthdate(candidate.birthdate());
        self.latitude(candidate.latitude());
        self.longitude(candidate.longitude());
        self.picture = candidate.picture;
        self.tags(candidate.tags());

        <!-- Do we have education information? -->
        if (candidate.education()[0]) {
            self.institution(candidate.education()[0].institution);
            self.degree(candidate.education()[0].degree);
            self.ed_start(candidate.education()[0].date_start);
            self.ed_end(candidate.education()[0].date_end);
            self.ed_desc(candidate.education()[0].description);
        } else {
            self.institution("");
            self.degree("");
            self.ed_start("");
            self.ed_end("");
            self.ed_desc("");
        }

        <!-- Do we have experience information? -->
        if (candidate.experience()[0]) {
            self.company(candidate.experience()[0].company);
            self.job_title(candidate.experience()[0].job_title);
            self.job_start(candidate.experience()[0].date_start);
            self.job_end(candidate.experience()[0].date_end);
            self.job_desc(candidate.experience()[0].description);
        } else {
            self.company("");
            self.job_title("");
            self.job_start("");
            self.job_end("");
            self.job_desc("");
        }

        $('edit').modal('show');
    }

    self.editCandidate = function() {
        $('#edit').modal('hide');

        edited = {
            name: self.name(),
            gender: parseInt(self.gender(), 10),
            email: self.email(),
            phone: self.phone(),
            address: self.address(),
            birthdate: self.birthdate(),
            latitude: parseFloat(self.latitude(), 10),
            longitude: parseFloat(self.longitude(), 10),
            picture: self.picture,
            tags: self.tags(),
            experience: [{
                'company': self.company(),
                'job_title': self.job_title(),
                'date_start': self.job_start(),
                'date_end': self.job_end(),
                'description': self.job_desc()
            }],
        }

        <!-- Do we have education data? -->
        if (self.institution() == "" && self.degree() == "" && self.ed_start() == "" && self.ed_end() == "" && self.ed_desc() == "") {
            edited['education'] = []
        } else {
            _education = {
                'institution': self.institution(),
                'degree': self.degree(),
                'date_start': self.job_start(),
                'date_end': self.job_end(),
                'description': self.job_desc()
            }
            edited['education'] = [_education]
        }

        <!-- Do we have experience data? -->
        if (self.company() == "" && self.job_title() == "" && self.job_start() == "" && self.job_end() == "" && self.job_desc() == "") {
            edited['experience'] = []
        } else {
            _experience = {
                'company': self.company(),
                'job_title': self.job_title(),
                'date_start': self.job_start(),
                'date_end': self.job_end(),
                'description': self.job_desc()
            };

            edited['experience'] = [_experience];
        }

        candidatesViewModel.edit(self.candidate, edited);

        <!-- Reset -->
        self.name("");
        self.gender("");
        self.email("");
        self.phone("");
        self.address("");
        self.birthdate("");
        self.latitude("");
        self.longitude("");
        self.picture = "";
        self.tags("");
        self.company("");
        self.job_title("");
        self.job_start("");
        self.job_end("");
        self.job_desc("");
        self.institution("");
        self.degree("");
        self.ed_start("");
        self.ed_end("");
        self.ed_desc("");
    }
}

var candidatesViewModel = new CandidatesViewModel();
var addCandidateViewModel = new AddCandidateViewModel();
var editCandidateViewModel = new EditCandidateViewModel();
ko.applyBindings(candidatesViewModel, $('#main')[0]);
ko.applyBindings(addCandidateViewModel, $('#add')[0]);
ko.applyBindings(editCandidateViewModel, $('#edit')[0]);