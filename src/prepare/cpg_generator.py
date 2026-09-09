import json
import os
import os.path
import platform
import re
import subprocess
import time

from .cpg_client_wrapper import CPGClientWrapper

# from ..data import datamanager as data


def funcs_to_graphs(funcs_path):
    client = CPGClientWrapper()
    # query the cpg for the dataset
    print(f"Creating CPG.")
    graphs_string = client(funcs_path)
    # removes unnecessary namespace for object references
    graphs_string = re.sub(
        r"io\.shiftleft\.codepropertygraph\.generated\.", "", graphs_string
    )
    graphs_json = json.loads(graphs_string)

    return graphs_json["functions"]


def graph_indexing(graph):
    name = graph["file"].split(".c")[0].split("/")[-1]
    idx = int(name) if name.isdigit() else int(time.time() * 1000)
    del graph["file"]
    return idx, {"functions": [graph]}


def joern_parse(joern_path, input_path, output_path, file_name):
    out_file = file_name + ".bin"

    cmd = [
        os.path.join(os.getcwd(), f"./{joern_path}joern-parse"),
        input_path,
        "--output",
        output_path + out_file,
    ]

    system = platform.system()
    if system == "Windows":
        cmd = ["cmd", "/c"] + cmd

    joern_parse_call = subprocess.run(
        cmd,
        stdout=subprocess.PIPE,
        text=True,
        check=True,
    )
    print(str(joern_parse_call))
    return out_file


def joern_create(joern_path, in_path, out_path, cpg_files):
    json_files = []
    for cpg_file in cpg_files:
        json_file_name = f"{cpg_file.split('.')[0]}.json"
        json_files.append(json_file_name)

        print(in_path + cpg_file)
        if os.path.exists(in_path + cpg_file):
            json_in = f"{os.path.abspath(in_path)}/{cpg_file}"
            json_out = f"{os.path.abspath(out_path)}/{json_file_name}"
            input_path = f"inputPath={json_in}"
            output_path = f"outputPath={json_out}"

            if platform.system() == "Windows":
                input_path = f'"{input_path}"'
                output_path = f'"{output_path}"'

            script_path = (
                f"{os.path.dirname(os.path.abspath(joern_path))}/graph-for-funcs.sc"
            )
            cmd = [
                os.path.join(os.getcwd(), f"./{joern_path}joern"),
                "--script",
                script_path,
                "--param",
                input_path,
                "--param",
                output_path,
            ]
            if platform.system() == "Windows":
                cmd = ["cmd", "/c"] + cmd

            subprocess.run(
                cmd,
                check=True,
            )
    return json_files


def json_process(in_path, json_file):
    if os.path.exists(in_path + json_file):
        with open(in_path + json_file) as jf:
            cpg_string = jf.read()
            cpg_string = re.sub(
                r"io\.shiftleft\.codepropertygraph\.generated\.", "", cpg_string
            )
            cpg_json = json.loads(cpg_string)
            container = [
                graph_indexing(graph)
                for graph in cpg_json["functions"]
                if graph["file"] != "N/A"
            ]
            return container
    return None


"""
def generate(dataset, funcs_path):
    dataset_size = len(dataset)
    print("Size: ", dataset_size)
    graphs = funcs_to_graphs(funcs_path[2:])
    print(f"Processing CPG.")
    container = [graph_indexing(graph) for graph in graphs["functions"] if graph["file"] != "N/A"]
    graph_dataset = data.create_with_index(container, ["Index", "cpg"])
    print(f"Dataset processed.")

    return data.inner_join_by_index(dataset, graph_dataset)
"""

# client = CPGClientWrapper()
# client.create_cpg("../../data/joern/")
# joern_parse("../../joern/joern-cli/", "../../data/joern/", "../../joern/joern-cli/", "gen_test")
# print(funcs_to_graphs("/data/joern/"))
"""
while True:
    raw = input("query: ")
    response = client.query(raw)
    print(response)
"""
