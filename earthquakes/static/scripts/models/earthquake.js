App.Models.Earthquake = Backbone.Model.extend({
    defaults: {
        primary_id: null,
        primary_slug: null,
        mag: null,
        place: null,
        title: 'Earthquake Title',
        date_time: null,
        updated: null,
        updated_raw: null,
        tz: null,
        url: null,
        felt: null,
        cdi: null,
        mmi: null,
        alert: null,
        status: null,
        tsunami: null,
        sig: null,
        resource_type: null,
        latitude: null,
        longitude: null,
        depth: null
    },

    //url: 'api/earthquakes/'

});