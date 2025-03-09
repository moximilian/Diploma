import FieldPropsMixin from './FieldPropsMixin'
export default {
    mixins: [FieldPropsMixin],
    props: {
        type: {
            type: String,
            validator: value => ['select', 'search'].includes(value),
            default: () => 'select',
        },
        search: { type: [String, Boolean], default: () => '' },
        options: { type: [Array, Object], default: () => [] },
        multiple: { type: Boolean, default: () => false },
        outFormat: { type: Function, default: null },
        keyFormat: { type: Function, default: null },
        showFormat: { type: Function, default: null },
        beforeSet: { type: Function, default: null },
        isLocalSearch: { type: Boolean, default: () => true },
        // isEscAvailable: { type: Boolean, default: () => true },
        isEmptyAvailable: { type: Boolean, default: () => true },
        disabledOptions: { type: [Boolean, Array], default: () => false },
    },
    emits: ['search', 'onOpened', 'onClosed', 'select', 'unSelect'],
}
