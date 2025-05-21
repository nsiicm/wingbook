<script setup>
import { onMounted, ref } from 'vue';
import { useRoute } from 'vue-router'; // Import useRoute to access route parameters
import { useToast } from 'primevue/usetoast';

import api from '@/axios';
import { useRouter } from 'vue-router';
const router = useRouter();

const toast = useToast();
const flight = ref({});
const dropdownPlanes = ref([]); // Ref to store planes for the dropdown
const dropdownPilots = ref([]); // Ref to store pilots for the dropdown
const dropdownPassengers = ref([]); // Ref to store passengers for the dropdown
const passengersCost = ref({}); // Ref to store passenger costs
const submitted = ref(false);
const flights = ref();

const route = useRoute(); // Get the current route object
const id = ref(route.params.id); // Access the 'id' parameter from the URL
onMounted(async () => {
    const [planesRes, pilotsRes, passengersRes] = await Promise.all([
        api.get('/planes/'),
        api.get('/people/?is_pilot=true'),
        api.get('/people/')
    ]);

    dropdownPlanes.value = planesRes.data;
    dropdownPilots.value = pilotsRes.data;
    dropdownPassengers.value = passengersRes.data;

    if (id.value !== 'new') {
        const flightRes = await api.get(`/flights/${id.value}`);
        api.get(`/flights/${id.value}`).then((response) => {
            const data = response.data;
            flight.value = {
                ...data,
                date: data.date ? new Date(data.date) : null
            };
        });

        flight.value = flightRes.data;

        // Match and replace references with dropdown options
        flight.value.plane = dropdownPlanes.value.find(p => p.id === flight.value.plane.id);
        flight.value.pilot_in_command = dropdownPilots.value.find(p => p.id === flight.value.pilot_in_command.id);
        //flight.value.passengers = dropdownPassengers.value.find(p => p.id === flight.value.passengers.id);

        flight.value.departure_time = removeSeconds(flight.value.departure_time);
        flight.value.arrival_time = removeSeconds(flight.value.arrival_time);
        flight.value.flight_duration = removeSeconds(flight.value.flight_duration);
        flight.value.se_duration = removeSeconds(flight.value.se_duration);
        flight.value.me_duration = removeSeconds(flight.value.me_duration);
        flight.value.multi_pilot_duration = removeSeconds(flight.value.multi_pilot_duration);
        flight.value.night_duration = removeSeconds(flight.value.night_duration);
        flight.value.ifr_duration = removeSeconds(flight.value.ifr_duration);
        flight.value.pilot_in_command_duration = removeSeconds(flight.value.pilot_in_command_duration);
        flight.value.copilot_duration = removeSeconds(flight.value.copilot_duration);
        flight.value.dual_duration = removeSeconds(flight.value.dual_duration);
        flight.value.instructor_duration = removeSeconds(flight.value.instructor_duration);
        flight.value.simulator_duration = removeSeconds(flight.value.simulator_duration);
        const inputMap = {};
        Object.keys(flight.value.passengers_perc).forEach(passengerId => {
            inputMap[passengerId] = flight.value.passengers_perc[passengerId];
        });
        flight.value.passengerInputs = inputMap;
        compute_passenger_costs()

    } else {
        flight.value.passengerInputs = {};
        console.log("New flight");
    }
});

function removeSeconds(time) {
    if (typeof time === 'string' && time.includes(':')) {
        const parts = time.split(':');
        return parts.length > 2 ? `${parts[0]}:${parts[1]}` : time; // Keep only hours and minutes
    }
    return time;
}

function formatDuration(value) {
    console.log("Initial value:", value)
    if (!value) {
        return "00:00:00";
    } else {
        // If value is a Date object, format it to HH:MM:SS
        if (value instanceof Date) {
            value = value.toTimeString().split(' ')[0]
        }
    }
    console.log(value)
    return value
}
function formatDateToLocalISO(date) {
    if (!(date instanceof Date)) date = new Date(date);
    const year = date.getFullYear();
    const month = String(date.getMonth() + 1).padStart(2, '0');
    const day = String(date.getDate()).padStart(2, '0');
    return `${year}-${month}-${day}`;
}

function saveflight() {
    submitted.value = true;

    // Helper function to format duration values

    const passengerMap = {};
    if (flight.passengerInputs) {
        Object.keys(flight.value.passengerInputs).forEach(passengerId => {
            passengerMap[passengerId] = flight.value.passengerInputs[passengerId];
        });
    }
    if (flight.value.landing_night_num === undefined) {
        flight.value.landing_night_num = 0;
    }
    if (flight.value.landing_day_num === undefined) {
        flight.value.landing_day_num = 0;
    }
    if (flight.value.ifr_apch_num === undefined) {
        flight.value.ifr_apch_num = 0;
    }
    console.log(passengerMap)
    flight.value.passengers_perc = passengerMap
    // Format all duration fields
    console.log(flight.value)
    flight.value.date = formatDateToLocalISO(flight.value.date);

    //flight.value.date = (flight.value.date instanceof Date)
    //    ? flight.value.date.toISOString().split('T')[0]
    //    : new Date(flight.value.date).toISOString().split('T')[0];
    flight.value.departure_time = formatDuration(flight.value.departure_time);
    flight.value.arrival_time = formatDuration(flight.value.arrival_time);
    flight.value.flight_duration = formatDuration(flight.value.flight_duration);
    flight.value.se_duration = formatDuration(flight.value.se_duration);
    flight.value.me_duration = formatDuration(flight.value.me_duration);
    flight.value.multi_pilot_duration = formatDuration(flight.value.multi_pilot_duration);
    flight.value.night_duration = formatDuration(flight.value.night_duration);
    flight.value.ifr_duration = formatDuration(flight.value.ifr_duration);
    flight.value.pilot_in_command_duration = formatDuration(flight.value.pilot_in_command_duration);
    flight.value.copilot_duration = formatDuration(flight.value.copilot_duration);
    flight.value.dual_duration = formatDuration(flight.value.dual_duration);
    flight.value.instructor_duration = formatDuration(flight.value.instructor_duration);
    flight.value.simulator_duration = formatDuration(flight.value.simulator_duration);

    flight.value.pilot_in_command = flight.value.pilot_in_command.id;
    flight.value.plane = flight.value.plane.id;
    if (flight.value.passengers) {
        flight.value.passengers = flight.value.passengers.map((passenger) => passenger.id); // Map passengers to their IDs
    } else {
        flight.value.passengers = [];
    }
    console.log("A")
    if (flight.value.id) {
        console.log("AA")
        console.log("B")
        api.put(`/flights/${flight.value.id}/`, flight.value)
            .then(() => {
                flight.value = {};
                toast.add({ severity: 'success', summary: 'Successful', detail: 'FlightUpdated', life: 3000 });
            })
            .catch((error) => {
                console.error(error);
                toast.add({ severity: 'error', summary: 'Error', detail: 'Failed to update flight', life: 3000 });
            });
    } else {
        if (
            true
        ) {
            console.log("C")
            api.post('/flights/', flight.value)
                .then((response) => {
                    flight.value = {};
                    toast.add({ severity: 'success', summary: 'Successful', detail: 'FlightCreated', life: 3000 });
                })
                .catch((error) => {
                    console.error(error);
                    toast.add({ severity: 'error', summary: 'Error', detail: 'Failed to create flight', life: 3000 });
                });
        }
    }
    router.push({ path: '/flights' })
}

function compute_price(flight) {
    if (flight.flight_duration && flight.plane && flight.plane.hour_price && flight.pilot_in_command && flight.price === undefined) {
        const timeParts = formatDuration(flight.flight_duration).split(':');
        const timeHoursFloat = parseInt(timeParts[0], 10) + parseInt(timeParts[1], 10) / 60;
        console.log("Time in hours:", timeHoursFloat);
        console.log("Plane price per hour:", flight.plane.hour_price);
        if (flight.pilot_in_command.is_instructor === true) {
            flight.price = (flight.plane.hour_price * timeHoursFloat + flight.plane.instructor_hour_price * timeHoursFloat).toFixed(2); // Ensure price is a float with 2 decimals
        } else {
            flight.price = (flight.plane.hour_price * timeHoursFloat).toFixed(2); // Ensure price is a float with 2 decimals
        }
        console.log("Computed price:", flight.price);
    }
    console.log(flight.price)
}

function compute_timings(flight) {
    if (flight.plane && flight.flight_duration) {
        if (flight.plane && flight.plane.single_engine === true) {
            flight.se_duration = flight.flight_duration;
            flight.me_duration = "00:00";
        }
        if (flight.plane && flight.plane.single_engine === false) {
            flight.me_duration = flight.flight_duration;
            flight.se_duration = "00:00";
        }
        if (flight.plane && flight.plane.single_pilot === false) {
            flight.multi_pilot_duration = flight.flight_duration;
        } else {
            flight.multi_pilot_duration = "00:00";
        }
    }
    console.log(flight.flight_duration)
    console.log(flight.pilot_in_command)
    console.log(flight.pilot_in_command && flight.flight_duration)
    if (flight.pilot_in_command && flight.flight_duration) {
        flight.copilot_duration = "00:00";
        flight.instructor_duration = "00:00";
        console.log("Pilot in command:", flight.pilot_in_command);
        if (flight.pilot_in_command.is_main_pilot === true) {
            console.log("Pilot in command duration:", flight.flight_duration);
            flight.pilot_in_command_duration = flight.flight_duration;
            flight.dual_duration = "00:00";
        }
        if (flight.pilot_in_command.is_instructor === true) {
            console.log("Dual duration:", flight.copilot_duration);
            flight.dual_duration = flight.flight_duration;
            flight.pilot_in_command_duration = "00:00";
        }
    }
}

function compute_passenger_costs() {
    passengersCost.value = {}; // Reset the passenger costs
    const totalCost = parseFloat(flight.value.price) || 0; // Ensure total cost is a number
    console.log("Total cost:", totalCost);
    const passengerInputs = flight.value.passengerInputs || {};
    let totalPercentage = 0
    const totalnumberOfPassengers = Object.keys(passengerInputs).length + 1;
    let numProcessedPassengers = 0;

    for (const passengerId in passengerInputs) {
        const percentage = parseFloat(passengerInputs[passengerId]) || 0; // Ensure percentage is a number
        const passengerCost = (totalCost * (percentage / 100)).toFixed(2); // Calculate cost for each passenger
        totalPercentage += percentage; // Accumulate total percentage
        passengersCost.value[passengerId] = passengerCost; // Store the cost in the object
        numProcessedPassengers++;
    }
    const remainingPercentage = 100 - totalPercentage;
    const remainingPassengers = totalnumberOfPassengers - numProcessedPassengers;
    if (remainingPassengers > 0) {
        const remainingCost = (totalCost * (remainingPercentage / 100)).toFixed(2);
        const costPerPassenger = (remainingCost / remainingPassengers).toFixed(2);
        for (const passengerId in passengerInputs) {
            if (!passengersCost.value[passengerId]) {
                passengersCost.value[passengerId] = parseFloat(costPerPassenger); // Assign the remaining cost to each passenger
            }
        }
    }
    console.log("Passenger costs:", passengersCost.value);
}

</script>

<template>

    <Fluid>
        <Button label="Submit" :fluid="false" @click="saveflight"></Button>
        <div class="flex flex-col md:flex-row gap-8">
            <div class="md:w-1/2">
                <div class="card flex flex-col gap-4">
                    <div class="font-semibold text-xl">Time and location</div>
                    <div class="grid grid-cols-12 gap-2">
                        <label for="date" class="flex items-center col-span-12 mb-2 md:col-span-2 md:mb-0">Date</label>
                        <div class="col-span-12 md:col-span-10">
                            <DatePicker id="date" :showIcon="true" :showButtonBar="true" v-model="flight.date"
                                :placeholder="'Select Date'" required="true" :invalid="submitted && !flight.date"
                                dateFormat="yy-mm-dd" />
                        </div>
                    </div>
                    <div class="grid grid-cols-12 gap-2">
                        <label for="departure_airport"
                            class="flex items-center col-span-12 mb-2 md:col-span-2 md:mb-0">Departure airport</label>
                        <div class="col-span-12 md:col-span-10">
                            <InputText id="departure_airport" v-model.trim="flight.departure_airport" required="true"
                                autofocus :invalid="submitted && !flight.departure_airport" fluid />
                        </div>
                    </div>
                    <div class="grid grid-cols-12 gap-2">
                        <label for="departure_time"
                            class="flex items-center col-span-12 mb-2 md:col-span-2 md:mb-0">Departure Time</label>
                        <div class="col-span-12 md:col-span-10">
                            <DatePicker id="departure_time" v-model="flight.departure_time" timeOnly fluid />
                        </div>
                    </div>
                    <div class="grid grid-cols-12 gap-2">
                        <label for="arrival_airport"
                            class="flex items-center col-span-12 mb-2 md:col-span-2 md:mb-0">Arrival airport</label>
                        <div class="col-span-12 md:col-span-10">
                            <InputText id="arrival_airport" v-model.trim="flight.arrival_airport" required="true"
                                autofocus :invalid="submitted && !flight.departure_airport" fluid />
                        </div>
                    </div>
                    <div class="grid grid-cols-12 gap-2">
                        <label for="arrival_time"
                            class="flex items-center col-span-12 mb-2 md:col-span-2 md:mb-0">Arrival Time</label>
                        <div class="col-span-12 md:col-span-10">
                            <DatePicker id="arrival_time" v-model="flight.arrival_time" timeOnly fluid />
                        </div>
                    </div>
                </div>

                <div class="card flex flex-col gap-4">
                    <div class="font-semibold text-xl">Passengers</div>
                    <div class="flex flex-col gap-2">
                        <label for="passengers">Select Passengers</label>
                        <MultiSelect id="passengers" v-model="flight.passengers" :options="dropdownPassengers"
                            optionLabel="last_name" placeholder="Select Passengers" :showCheckbox="true"
                            @update:model-value="(value) => {
                                console.log(flight.passengers)
                            }" />
                    </div>
                    <div class="flex flex-col gap-4">
                        <div v-for="(passenger, index) in flight.passengers" :key="passenger.id"
                            class="flex flex-col gap-2">
                            <label :for="'passenger_' + passenger.id" class="block font-bold mb-2">
                                {{ passenger.last_name }}'s Input
                            </label>
                            <div class="flex gap-2 items-center">
                                <InputNumber :id="'passenger_' + passenger.id"
                                    v-model="flight.passengerInputs[passenger.id]" placeholder="Enter a number"
                                    required="true" fluid @update:model-value="compute_passenger_costs" />
                                <InputNumber :id="'passenger_disabled_' + passenger.id"
                                    v-model="passengersCost[passenger.id]" disabled :useGrouping="false"
                                    :minFractionDigits="2" :maxFractionDigits="2" fluid />

                            </div>
                        </div>
                    </div>
                </div>
            </div>
            <div class="md:w-1/2">
                <div class="card flex flex-col gap-4">
                    <div class="font-semibold text-xl">Flight Info</div>
                    <div class="grid grid-cols-12 gap-2">
                        <label for="date" class="flex items-center col-span-12 mb-2 md:col-span-2 md:mb-0">Plane</label>
                        <div class="col-span-12 md:col-span-10">
                            <Select v-model="flight.plane" :options="dropdownPlanes" optionLabel="registration_number"
                                placeholder="Select" @update:model-value="() => {
                                    compute_price(flight)
                                    compute_timings(flight)
                                }" />
                        </div>
                    </div>
                    <div class="grid grid-cols-12 gap-2">
                        <label for="departure_airport"
                            class="flex items-center col-span-12 mb-2 md:col-span-2 md:mb-0">Pilot in command</label>
                        <div class="col-span-12 md:col-span-10">
                            <Select v-model="flight.pilot_in_command" :options="dropdownPilots" optionLabel="last_name"
                                placeholder="Select" @update:model-value="() => {
                                    compute_timings(flight)
                                    compute_price(flight)
                                }" />
                        </div>
                    </div>
                    <div class="grid grid-cols-12 gap-2">
                        <label for="departure_time"
                            class="flex items-center col-span-12 mb-2 md:col-span-2 md:mb-0">Flight Duration</label>
                        <div class="col-span-12 md:col-span-10">
                            <DatePicker id="flight_duration" v-model="flight.flight_duration" timeOnly fluid
                                @update:model-value="() => {
                                    compute_timings(flight)
                                    compute_price(flight)
                                }" />
                        </div>
                    </div>
                    <div class="grid grid-cols-12 gap-2">
                        <label for="arrival_airport"
                            class="flex items-center col-span-12 mb-2 md:col-span-2 md:mb-0">Price</label>
                        <div class="col-span-12 md:col-span-10">
                            <InputText id="price" v-model.trim="flight.price" required="true" autofocus
                                :invalid="submitted && !flight.price" fluid />
                        </div>
                    </div>
                    <div class="grid grid-cols-12 gap-2">
                        <label for="arrival_airport"
                            class="flex items-center col-span-12 mb-2 md:col-span-2 md:mb-0">Landing Day</label>
                        <div class="col-span-12 md:col-span-10">
                            <InputNumber id="landing_day_num" v-model.trim="flight.landing_day_num" required="true"
                                autofocus fluid />
                        </div>
                    </div>
                    <div class="grid grid-cols-12 gap-2">
                        <label for="arrival_airport"
                            class="flex items-center col-span-12 mb-2 md:col-span-2 md:mb-0">Landing Night</label>
                        <div class="col-span-12 md:col-span-10">
                            <InputNumber id="landing_night_num" v-model.trim="flight.landing_night_num" required="true"
                                autofocus fluid />
                        </div>
                    </div>
                    <div class="grid grid-cols-12 gap-2">
                        <label for="arrival_airport"
                            class="flex items-center col-span-12 mb-2 md:col-span-2 md:mb-0">IFR Approach</label>
                        <div class="col-span-12 md:col-span-10">
                            <InputNumber id="ifr_apch_num" v-model.trim="flight.ifr_apch_num" required="true" autofocus
                                fluid />
                        </div>
                    </div>

                </div>
                <div class="card flex flex-col gap-4">
                    <div class="font-semibold text-xl">Timings</div>
                    <div class="grid grid-cols-12 gap-2">
                        <label for="se_duration" class="flex items-center col-span-12 mb-2 md:col-span-2 md:mb-0">SE
                            Duration
                        </label>
                        <div class="col-span-12 md:col-span-10">
                            <DatePicker id="se_duration" v-model="flight.se_duration" timeOnly fluid
                                :disabled="flight.plane && flight.flight_duration" />
                        </div>
                    </div>
                    <div class="grid grid-cols-12 gap-2">
                        <label for="me_duration" class="flex items-center col-span-12 mb-2 md:col-span-2 md:mb-0">ME
                            Duration</label>
                        <div class="col-span-12 md:col-span-10">
                            <DatePicker id="me_duration" v-model="flight.me_duration" timeOnly fluid
                                :disabled="flight.plane && flight.flight_duration" />
                        </div>
                    </div>
                    <div class="grid grid-cols-12 gap-2">
                        <label for="multi_pilot_duration"
                            class="flex items-center col-span-12 mb-2 md:col-span-2 md:mb-0">Multi Pilot
                            Duration</label>
                        <div class="col-span-12 md:col-span-10">
                            <DatePicker id="multi_pilot_duration" v-model="flight.multi_pilot_duration" timeOnly fluid
                                :disabled="flight.plane && flight.flight_duration" />
                        </div>
                    </div>
                    <div class="grid grid-cols-12 gap-2">
                        <label for="night_duration"
                            class="flex items-center col-span-12 mb-2 md:col-span-2 md:mb-0">Night Duration</label>
                        <div class="col-span-12 md:col-span-10">
                            <DatePicker id="night_duration" v-model="flight.night_duration" timeOnly fluid />
                        </div>
                    </div>
                    <div class="grid grid-cols-12 gap-2">
                        <label for="ifr_duration" class="flex items-center col-span-12 mb-2 md:col-span-2 md:mb-0">IFR
                            Duration</label>
                        <div class="col-span-12 md:col-span-10">
                            <DatePicker id="ifr_duration" v-model="flight.ifr_duration" timeOnly fluid />
                        </div>
                    </div>
                    <div class="grid grid-cols-12 gap-2">
                        <label for="pilot_in_command_duration"
                            class="flex items-center col-span-12 mb-2 md:col-span-2 md:mb-0">Pilot in Command
                            Duration</label>
                        <div class="col-span-12 md:col-span-10">
                            <DatePicker id="pilot_in_command_duration" v-model="flight.pilot_in_command_duration"
                                timeOnly fluid :disabled="flight.plane && flight.flight_duration" />
                        </div>
                    </div>
                    <div class="grid grid-cols-12 gap-2">
                        <label for="copilot_duration"
                            class="flex items-center col-span-12 mb-2 md:col-span-2 md:mb-0">Co-Pilot Duration</label>
                        <div class="col-span-12 md:col-span-10">
                            <DatePicker id="copilot_duration" v-model="flight.copilot_duration" timeOnly fluid
                                :disabled="flight.plane && flight.flight_duration" />
                        </div>
                    </div>
                    <div class="grid grid-cols-12 gap-2">
                        <label for="dual_duration" class="flex items-center col-span-12 mb-2 md:col-span-2 md:mb-0">Dual
                            Duration</label>
                        <div class="col-span-12 md:col-span-10">
                            <DatePicker id="dual_duration" v-model="flight.dual_duration" timeOnly fluid
                                :disabled="flight.plane && flight.flight_duration" />
                        </div>
                    </div>
                    <div class="grid grid-cols-12 gap-2">
                        <label for="instructor_duration"
                            class="flex items-center col-span-12 mb-2 md:col-span-2 md:mb-0">Instructor Duration</label>
                        <div class="col-span-12 md:col-span-10">
                            <DatePicker id="instructor_duration" v-model="flight.instructor_duration" timeOnly fluid
                                :disabled="flight.plane && flight.flight_duration" />
                        </div>
                    </div>
                </div>
            </div>
        </div>
    </Fluid>
</template>