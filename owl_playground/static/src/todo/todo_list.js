/** @odoo-module */
// import { useAutofocus } from "@web/core/utils/hooks";

import { Component ,useState , useRef, onPatched, onMounted } from "@odoo/owl" ;
import { Todoitem } from "./todo_item" ;
import { input_focus1 } from "../utils";


export class Todolist extends Component {

    static template = "owl_playground.TodoList";
    static components = { Todoitem };

    setup(){
        this.todos = useState([]);
        this.input1 = useRef("input_focus");
        
        // new input_focus1().test(this.input1);        // instance for second method of using onMount
        
        onMounted(() => {
            return new input_focus1().test(this.input1);
         });
    };

    addtodo(ev){
        if(ev.keyCode === 13 && ev.target.value != "" ){
            let v_id = this.todos[(this.todos.length)-1] ?  this.todos[(this.todos.length)-1].id + 1 : 1 ;
            this.todos.push({
                id: v_id,
                description : " " + ev.target.value,
                isCompleted: false});
            
            ev.target.value = " ";
        }
    }

    stateAlter(id123) {
        for(let a=0; a<this.todos.length;a++){                                      //first method
            if(this.todos[a].id == id123){
                this.todos[a].isCompleted = !this.todos[a].isCompleted;
            }
        }

        //Second method
        // toggleTodo(todoId) {
        //     const todo = this.todos.find((todo) => todo.id === todoId);
        //     if (todo) {
        //         todo.isCompleted = !todo.isCompleted;
        //     }
        // }
    }

    delelte_todo(todoId){
        const obj_ele = this.todos.find((todo)=> todo.id === todoId);
        const index = this.todos.findIndex(x => x === obj_ele);
        // debugger;

        this.todos.splice(index, 1);
        // delete this.todos.obj_ele;
    }    

}


