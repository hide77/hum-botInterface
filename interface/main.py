#!/usr/bin/env python

import path_util        # noqa: F401
import asyncio
import errno
import socket

from socket_interface import sio, setHummingInstance

from typing import (
    List,
    Coroutine
)

from hummingbot.client.hummingbot_application import HummingbotApplication
from hummingbot.client.config.global_config_map import global_config_map
from hummingbot.client.config.config_helpers import (
    create_yml_files,
    read_configs_from_yml
)
from hummingbot import (
    init_logging,
    check_dev_mode,
    chdir_to_data_directory
)
from hummingbot.client.ui.stdout_redirection import patch_stdout
from hummingbot.core.utils.async_utils import safe_gather
from hummingbot.core.utils.exchange_rate_conversion import ExchangeRateConversion


#//////////////////////////////////////////
async def main():
    chdir_to_data_directory()

    await create_yml_files()

    # This init_logging() call is important, to skip over the missing config warnings.
    init_logging("hummingbot_logs.yml")
    hb = HummingbotApplication.main_application()
    setHummingInstance(hb)

    read_configs_from_yml()
    ExchangeRateConversion.get_instance().start()

    with patch_stdout(log_field=hb.app.log_field):
        dev_mode = check_dev_mode()
        if dev_mode:
            hb.app.log("Running from dev branches. Full remote logging will be enabled.")
        init_logging("hummingbot_logs.yml",
                     override_log_level=global_config_map.get("log_level").value,
                     dev_mode=dev_mode)
        tasks: List[Coroutine] = [hb.run(),sio.connect('ws://localhost:5000')]
        await safe_gather(*tasks)

if __name__ == "__main__":
    ev_loop: asyncio.AbstractEventLoop = asyncio.get_event_loop()
    ev_loop.run_until_complete(main())
