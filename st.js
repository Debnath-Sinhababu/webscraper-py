let t = [
    "Login successful.\n",
    "Dashboard Data:\n",
    "[\n",
    "    {\n",
    "        \"id\": \"251423376\",\n",
    "        \"uid\": \"1f66a34b-6bd7-4937-a329-e07cf8635e5d\",\n",
    "        \"pickup\": \"23 Aug\",\n",
    "        \"age\": \"10s\",\n",
    "        \"origin\": \"Youngsville\",\n",
    "        \"destination\": null,\n",
    "        \"weight\": \"5k\",\n",
    "        \"distance\": \"355 mi\",\n",
    "        \"price\": \"forecast\",\n",
    "        \"company\": \"TQL\",\n",
    "        \"phone\": \"(800) 580-3101 x 8\"\n",
    "    },\n",
    "    {\n",
    "        \"id\": \"251423375\",\n",
    "        \"uid\": \"81cfa9aa-1dc6-42a7-964e-a0f31f16d438\",\n",
    "        \"pickup\": \"23 Aug\",\n",
    "        \"age\": \"11s\",\n",
    "        \"origin\": \"Durham\",\n",
    "        \"destination\": null,\n",
    "        \"weight\": \"43k\",\n",
    "        \"distance\": \"450 mi\",\n",
    "        \"price\": \"show\",\n",
    "        \"company\": \"TQL\",\n",
    "        \"phone\": \"(800) 580-3101 x 8\"\n",
    "    }\n",
    "]"
];

let t2 = '';

for (let index = 0; index < t.length; index++) {
    const element = t[index];

    if(element.includes(']')) {
        t2 += ']';
        break;
    }

    if(t2 != '' || element.includes('[')) {
        t2 += element.replace('\n', '').trim();
    }
}

console.log(t2);