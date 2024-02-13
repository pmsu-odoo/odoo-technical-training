/** @odoo-module */

import { Component, markup ,useState} from "@odoo/owl";
import { Counter} from './counter/counter';
import { Card } from './card/card';
import { Todolist } from "./todo/todo_list";


export class Playground extends Component {
    debugger;
    setup(){
        this.state = useState({sum : 0});
        this.str1 = "<div class='text-primary'>some content</div>";
        this.str2 = markup("<div class='text-primary'>some content</div>");
    };
    
    static props = {
        onChange: { type: Function, optional: true },
    };

    static template = "owl_playground.playground";
    static components = { Counter , Card , Todolist } ;
    

    incrementSum() {
        return this.state.sum++;
    };
   
}