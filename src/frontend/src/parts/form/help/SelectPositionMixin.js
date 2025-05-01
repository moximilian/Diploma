import mitt from 'mitt'
import { addGroupEventListeners } from '@/core/functions'
const emitter = mitt()

export default {
    computed: {
        optionKeys() {
            return this.isArray
                ? this.optionList.map(val => this.getKey(val))
                : Object.keys(this.optionList)
        },
        parentPageEl() {
            return document.querySelector('.page')
        },
    },
    methods: {
        moveUp() {
            if (null === this.pos) this.pos = 0
            else {
                this.pos--
                if (this.pos < 0) this.pos = this.optionKeys.length - 1
            }
        },
        moveDown() {
            if (null === this.pos) this.pos = 0
            else {
                this.pos++
                if (this.pos >= this.optionKeys.length) this.pos = 0
            }
        },
        selectKeyboardHovered() {
            if (this.pos === null) return
            this.select(this.optionKeys[this.pos])
        },
        setPosition(changeDisplay = true, changePosition = false, leftOffset = 0) {
            const movableElem = this.$refs.movableElem
            if (!movableElem)
                return setTimeout(
                    () => this.setPosition(changeDisplay, changePosition, leftOffset),
                    100
                )
            const triggerElem = this.$refs.triggerElem

            if (changeDisplay) movableElem.style.display = 'block'
            movableElem.style.visibility = 'visible'

            const scrollY = window.scrollY
            const triggerRect = triggerElem.getBoundingClientRect()
            const movableRect = movableElem.getBoundingClientRect()
            const top = triggerRect.y + triggerRect.height
            const bottom = top + movableRect.height

            const heightOffset = changePosition ? triggerRect.width : 0

            movableElem.style.top = `${
                (window.innerHeight < bottom - heightOffset
                    ? triggerRect.y - movableRect.height + heightOffset
                    : top - heightOffset) + scrollY
            }px`
            movableElem.style.left = `${triggerRect.x + heightOffset - leftOffset}px`
            if (changeDisplay) movableElem.style.width = `${triggerRect.width}px`
        },
        close() {
            this.opened = false
            // this.parentPageEl.removeEventListener('scroll', this.close)
        },
    },
    created() {
        const keys = {
            Escape: e => this.isEscAvailable && this.close(e),
            ArrowUp: this.moveUp,
            ArrowDown: this.moveDown,
            Enter: this.selectKeyboardHovered,
        }
        let controller = addGroupEventListeners(document, {
            mousedown: e => {
                const dropDown = this.$refs?.movableElem
                this.opened &&
                    !this.$el.contains(e.target) &&
                    !dropDown?.contains(e.target) &&
                    this.close(e)
            },
            keydown: e => this.opened && keys[e.code]?.(e),
        })
        // в изначальном коде было this.parentPageEl.removeEventListener('scroll', this.close), поэтому решил добавить это, но не увидел где слушатель добавляется, поэтому закомментировал
        this.parentPageEl &&
            (controller = addGroupEventListeners(
                this.parentPageEl,
                {
                    scroll: this.close,
                },
                controller
            ))

        emitter.on('hook:beforeDestroy', controller.abort)
    },
}
