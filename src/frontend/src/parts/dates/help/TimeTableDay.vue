<template>
    <div class="timetable-day" :key="currentMinute" ref="timetable">
        <div
            class="block"
            v-for="index of blocks"
            :key="index"
            :style="{ height: blockSizeMins + 'px' }"
        >
            <div class="block" v-if="index % blocksInHour == 0 && currentTimeBlock !== index">
                <div class="semi-transparent-black-color" v-if="isShowHours">
                    {{ getHour(index) }}
                </div>
                <div class="line"></div>
            </div>
            <div class="block" v-if="currentTimeBlock === index">
                <div class="current-time" v-if="isShowHours">{{ new Date().toShowTime() }}</div>
                <div
                    class="line-current-time"
                    :class="{ ['semi-transparent']: !isShowCurrTimeLine }"
                ></div>
            </div>
        </div>
        <div
            class="events-blocks"
            v-if="events.length > 0"
            :style="{ marginLeft: (isShowHours ? 45 : 0) + 'px' }"
        >
            <div
                class="event-block-wrapper"
                v-for="(event, index) of events"
                :key="index"
                :style="{ zIndex: index + 1 }"
                @click="$router.push('/events/show/' + event.id)"
            >
                <div class="event-block" :ref="'event_' + index + currentDay.toShowDate()">
                    <div class="event-title">
                        {{ event.name }}
                        {{ getEventFullDate(event.start_date, event.start_time).toShowTime() }}
                        -
                        {{ getEventFullDate(event.start_date, event.end_time).toShowTime() }}
                    </div>
                    <div v-if="!fromWeek">Цена {{ event.price }} руб.</div>
                    <div v-if="!fromWeek">
                        Группа
                        <ValueToString
                            :field="{
                                displayName: 'groups',
                                localKeyName: 'group_id',
                                showName: 'name',
                            }"
                            :row="event"
                        />
                    </div>
                </div>
            </div>
        </div>
    </div>
</template>

<script>
import ValueToString from '@/parts/table/parts/ValueToString.vue'
export default {
    props: {
        currentDay: { type: Array, default: () => [] },
        blockSizeMins: { type: Number, default: () => 15 },
        isShowHours: { type: Boolean, default: () => true },
        fromWeek: { type: Boolean, default: () => false },
        isShowCurrTimeLine: { type: Boolean, default: () => true },

        events: { type: Array, default: () => [] },
    },
    data() {
        return {
            blocksInHour: 10,
            currentTimeBlock: 0,
            debug: false,
            topPadding: 0,
            blocksColors: ['var(--main-color)', 'pink', 'blue', 'violed', 'green'],
            maxWidth: 0,
        }
    },
    watch: {
        eventsItems() {
            this.setEventsStyles()
        },
        currentDay() {
            this.setEventsStyles()
        },
    },
    methods: {
        getHour(index) {
            let hours = (index / this.blocksInHour + 1) % 24
            if (hours.toString().length === 1) hours = `0${hours}`
            return `${hours}:00`
        },
        getTimeBlock(date = null) {
            date = date ? new Date(date) : new Date()
            let newIndex = (date.getHours() - 1) * this.blocksInHour - 1
            const mins = date.getMinutes()
            newIndex += Math.ceil((mins * this.blocksInHour) / 60)
            return newIndex
        },
        getEventFullDate(date, time) {
            date = new Date(date)
            const hours = time.split(':').map(item => parseInt(item))
            const newDate = date.setHours(hours[0], hours[1], hours[2])
            return new Date(newDate)
        },
        getTimeTableYOffset() {
            const timetableEl = this.$refs.timetable
            const timetableRect = timetableEl?.getBoundingClientRect()
            this.topPadding = Math.abs(timetableRect?.y ?? 0)
            this.maxWidth = Math.abs(timetableRect?.width ?? 0)
        },
        setEventStyles(event, index) {
            const startBlock =
                this.getTimeBlock(this.getEventFullDate(event.start_date, event.start_time)) + 1

            const endBlock = this.getTimeBlock(
                this.getEventFullDate(event.start_date, event.end_time)
            ) + 1

            const startTop = startBlock * this.blockSizeMins
            const endTop = endBlock * this.blockSizeMins + 1

            const height = endTop - startTop - this.blockSizeMins

            const eventEl = this.$refs['event_' + index + this.currentDay.toShowDate()]?.[0]
            if (!eventEl) return setTimeout(() => this.setEventStyles(event, index), 100)

            if (eventEl) {
                eventEl.style.height = height + 'px'
                if (eventEl.style.height < height) eventEl.style.height = height
                eventEl.style.top = this.topPadding + startTop + 18 + 'px'
                eventEl.style.backgroundColor = this.blocksColors[index % 5]
                const width = this.maxWidth -
                    (this.isShowHours ? 45 : 0) -
                    (this.fromWeek ? 0 : 22) -
                    24
                eventEl.style.width = width + 'px'
            }
        },
        setEventsStyles() {
            const timetableEl = this.$refs.timetable
            const timetableRect = timetableEl?.getBoundingClientRect()
            this.maxWidth = Math.abs(timetableRect?.width ?? 0)
            this.eventsItems.forEach(this.setEventStyles)
        },
    },
    computed: {
        blocks() {
            return [...Array(24 * this.blocksInHour).keys()]
        },
        eventsItems() {
            return this.events
        },
    },
    created() {
        this.blocksInHour = Math.trunc(60 / this.blocksInHour) - 1
        this.currentTimeBlock = this.getTimeBlock()
    },
    mounted() {
        window.scrollTo({ top: 0 })
        this.getTimeTableYOffset()
        this.setEventsStyles()
    },
    components: { ValueToString },
}
</script>
