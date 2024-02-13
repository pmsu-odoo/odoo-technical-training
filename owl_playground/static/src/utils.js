/** @odoo-module */

// import { useAutofocus } from "@web/core/utils/hooks";            // throughs error : Missing dependencies: ['@web/core/utils/hooks']

import {Component, onMounted} from '@odoo/owl';

export class input_focus1 extends Component {

    test(aa) {
        aa.el.focus();
        
        // onMounted(() => {                    // second method for using onmount
        //     aa.el.focus();
        //  });
    }    
}