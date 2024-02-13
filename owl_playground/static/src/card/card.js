/** @odoo-module **/

import { Component ,useState} from "@odoo/owl";

export class Card extends Component {
    static template = "owl_playground.card";
    static props = {
        title : String,
        content : String
    }

    setup(){
        this.state = useState({isopen : true});
    }

    minimize(){
        // debugger;
        this.state.isopen = !this.state.isopen; 
        // debugger;
    }
}