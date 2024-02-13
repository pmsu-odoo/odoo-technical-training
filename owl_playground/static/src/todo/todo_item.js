/** @odoo-module */

import { Component } from "@odoo/owl";

export class Todoitem extends Component {

    static template = "owl_playground.todoitem" ;
    static props = {
        todo : { type : Object , shape : { id: Number , description: String , isCompleted: Boolean }},
        toggleState : Function,
        removeTodo : Function,

    };

    onChange1(ev) {
        this.props.toggleState(this.props.todo.id);
    };

    remove_todo(){
    this.props.removeTodo(this.props.todo.id);
    };
}