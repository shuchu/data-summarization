# -*- coding: utf-8 -*-


import argparse
import csv
import glob
import json
import logging
import os
import sys

from summ.counter import Counter
from summ.kv_stores.dict_store import DictStore
from summ.metrics import Metric

logging.basicConfig(
    format="%(asctime)s %(name)s %(levelname)s: %(message)s",
    datefmt="%m/%d/%Y %I:%M:%S %p",
    encoding="utf-8",
    level=logging.DEBUG,
)
_logger = logging.getLogger(__name__)


def summerizer(
    data_folder: str,
    out_dir: str = "./result",
    out_fmt: str = "csv",
    eval_key: str = "*",
    eval_type: str = "",
    metrics: str = "*",
) -> None:
    """Summarize the data in data_folder.
        Supported output file format: .csv, .json.

    Args:
        data_folder: the folder includes all data file.
        out_dir: the output directory.
        out_fmt: the output file format.
        device_id: the id of device.
        event_type: the type of event.
        metrics: the metrics represented in string format, for example 'min,max'.
    """
    _logger.info(
        f"analyzing folder: {data_folder} with output directory: {out_dir}, format: {out_fmt}, key: {eval_key}, type: {eval_type} and metrics: {metrics}."
    )

    _supported_output_fmt = {"csv", "json"}

    if metrics == "*" or not metrics:
        list_of_metrics = ["*"]
    else:
        list_of_metrics = metrics.strip().split(",")

    my_kvstore = DictStore()
    mycounter = Counter(my_kvstore)

    # Iterative check the .csv file in the data_folder.
    # And update the count to a KV store.
    for f in glob.iglob(os.path.join(data_folder, "ev_dump_*.csv"), recursive=True):
        mycounter.update_by_file(f, header=True)

    # Calculate the metrics
    mycalc = Metric(my_kvstore)
    res = mycalc.calc_stats(
        eval_key=eval_key, eval_type=eval_type, metrics=list_of_metrics
    )

    if not res:
        _logger.warning("The final calculated distribution is empty.")
    else:
        # Output to the target folder
        target_dir = "./"
        target_fmt = ".csv"
        if out_dir:
            target_dir = out_dir

        out_fmt = out_fmt.lower()
        if out_fmt in _supported_output_fmt:
            target_fmt = out_fmt

        if out_fmt == "csv":
            targt_fname = "dist_{}.csv" % eval_key
            try:
                target_path = os.path.join(target_dir, target_fname)
                with open(target_path, "w") as f:
                    mywriter = csv.writer(f)
                    mywriter.writerow([res[eval_key][m] for m in list_of_metrics])
            except Exception as e:
                _logger.error(
                    "Failed to write the result to diretory: {}, error: {}"
                    % (target_path, e)
                )
        elif out_fmt == "json":
            target_fname = "dist_{}.json" % eval_key
            try:
                target_path = os.path.join(target_dir, target_fname)
                with open(target_path, "w") as f:
                    json.dump(res, f, ensure_ascii=False)
            except Exception as e:
                _logger.error(
                    "Failed to write the result to diretory: {}, error: {}"
                    % (target_path, e)
                )


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Summarize the data in a folder.")
    parser.add_argument("folder", help="a folder contains data files.")
    parser.add_argument(
        "--output_dir", help="the output directory to store analysis results."
    )
    parser.add_argument(
        "--output_fmt", help="the format of analysis results. Default CSV."
    )
    parser.add_argument("--eval_key", help="the key about to be analyzed.")
    parser.add_argument("--eval_type", help="the type of the related key.")
    parser.add_argument(
        "--metrics",
        help="the list of metrics to be calculated. Represented by a joined string separated by commas.",
    )

    args = parser.parse_args()

    out_dir = "./"
    if args.output_dir:
        out_dir = args.output_dir

    out_fmt = "csv"
    if args.output_fmt:
        out_fmt = args.output_fmt

    eval_key = "*"
    if args.eval_key:
        eval_key = args.eval_key

    eval_type = ""
    if args.eval_type:
        eval_type = args.eval_type

    metrics = "*"
    if args.metrics:
        metrics = args.metrics

    summerizer(args.folder, out_dir, out_fmt, eval_key, eval_type, metrics)
