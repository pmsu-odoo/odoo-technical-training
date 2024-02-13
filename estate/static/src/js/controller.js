/** @odoo-module **/
import publicWidget from "web.public.widget";
// import { rpc } from "@web/core/network/rpc";
var rpc = require('web.rpc');

console.log("test");
publicWidget.registry.offerwidget = publicWidget.Widget.extend({
    selector: ".container",
    events: {
        "click .offer_class": "_onReorder123",
    },

    async _onReorder123(ev) {

        // var model = 'estate.property';
        // var domain = [];
        // var fields = [];
        // rpc.query({
        //     model: model,
        //     method: 'search_read',
        //     args: [domain, fields],
        // }).then(function (data) {
        //     console.log(data);
        // });
        // debugger;

        // debugger;

        // var defs = [];
        // var def = await rpc.query({
        //     model: 'estate.property',
        //     method: 'total_offer',
        // })
        // debugger;
        // defs.push(def);
        // debugger;this.do_action['valueOf']
        
        var model = 'estate.property';
        // var domain = [];
        // var fields = [];

        // rpc.query({
        //     model: model,
        //     method: 'total_offer',
        //     args: [domain, fields],
        // }).then(function (data) {
        //     console.log(data);});

        debugger;
        var id = document.activeElement.attributes['data-id'].value;
        return await this._rpc({
            route: '/real_estate/',
            
            // model: model,
            // method: 'search_read',
            // args:[[]]
            // args: [[['id','=',parseInt(id)]], ['title']],
        })

        console.log(result);
    },

    test(ev){
        var result = this._onReorder123();
    }
    
});