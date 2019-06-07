"""Provides a base class for CampaignDBs

"""

__copyright__ = """

    Copyright 2018 Robin A. Richardson, David W. Wright

    This file is part of EasyVVUQ

    EasyVVUQ is free software: you can redistribute it and/or modify
    it under the terms of the Lesser GNU General Public License as published by
    the Free Software Foundation, either version 3 of the License, or
    (at your option) any later version.

    EasyVVUQ is distributed in the hope that it will be useful,
    but WITHOUT ANY WARRANTY; without even the implied warranty of
    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
    Lesser GNU General Public License for more details.

    You should have received a copy of the Lesser GNU General Public License
    along with this program.  If not, see <https://www.gnu.org/licenses/>.

"""
__license__ = "LGPL"


class BaseCampaignDB:
    """Baseclass for all EasyVVUQ CampaignDBs

    Skeleton for class that provides database access for the campaign.

    Parameters
    ----------
    location: str or None
        Location to look for database.
    new_campaign: bool
        Does the database need to be initialised as a new campaign.
    name: str or None
        Name of the campaign.
    info: `easyvvuq.data_structs.CampaignInfo`
        Information defining the campaign.
    """

    def __init__(self, location=None, new_campaign=False, name=None, info=None):
        pass

    def app(self, name):
        """
        Get app information. Specific applications selected by `name`,
        otherwise first entry in database 'app' selected.

        Parameters
        ----------
        name : str or None
            Name of selected app, if `None` given then first app will be
            selected.

        Returns
        -------
        dict:
            Application information.
        """

        raise NotImplementedError

    def add_app(self, app_info):
        """
        Add application to the 'app' table.

        Parameters
        ----------
        app_info: AppInfo
            Application definition.

        Returns
        -------

        """

        raise NotImplementedError

    def add_sampler(self, sampler):
        """
        Add new Sampler to the 'sampler' table.

        Parameters
        ----------
        sampler_element: BaseSamplingElement

        Returns
        -------

        """

        raise NotImplementedError

    def update_sampler(self, sampler_id, sampler_element):
        raise NotImplementedError

    def resurrect_sampler(self, sampler_id):
        raise NotImplementedError

    def set_campaign_collater(self, collater, campaign_id):
        raise NotImplementedError

    def resurrect_collation(self, campaign_id):
        raise NotImplementedError

    def resurrect_app(self, app_name):
        raise NotImplementedError

    def add_run(self, run_info=None, prefix='Run_'):
        """
        Add run to the `runs` table in the database.

        Parameters
        ----------
        run_info: `easyvvuq.data_structs.RunInfo`
            Contains relevant run fields: params, status (where in the
            EasyVVUQ workflow is this RunTable), campaign (id number),
            sample, app
        prefix: str
            Prefix for run id

        Returns
        -------

        """
        raise NotImplementedError

    def set_dir_for_run(self, run_name, run_dir, campaign=None, sampler=None):
        raise NotImplementedError

    def run(self, run_name, campaign=None, sampler=None):
        """
        Get the information for a specified run.

        Parameters
        ----------
        run_name: str
            Name of run to filter for.
        campaign:  int or None
            Campaign id to filter for.
        sampler: int or None
            Sample id to filter for.

        Returns
        -------
        dict
            Containing run information (run_name, params, status, sample,
            campaign, app)
        """
        raise NotImplementedError

    def campaigns(self):
        """Get list of campaigns for which information is stored in the
        database.

        Returns
        -------
        list:
            Campaign names.
        """
        raise NotImplementedError

    def campaign_dir(self, campaign_name=None):
        """Get campaign directory for `campaign_name`.

        Returns
        -------
        str:
            Path to campaign directory.
        """
        raise NotImplementedError

    def runs(self, campaign=None, sampler=None, status=None, not_status=None):
        """
        A generator to return all run information for selected `campaign` and `sampler`.

        Parameters
        ----------
        campaign: int or None
            Campaign id to filter for.
        sampler: int or None
            Sampler id to filter for.
        status: enum(Status) or None
            Status string to filter for.
        not_status: enum(Status) or None
            Exclude runs with this status string

        Returns
        -------
        dict:
            Information on each selected run (key = run_name, value = dict of
            run information fields.), one at a time.
        """

        raise NotImplementedError

    def runs_dir(self, campaign_name=None):
        """
        Get the directory used to store run information for `campaign_name`.

        Parameters
        ----------
        campaign_name: str
            Name of the selected campaign.

        Returns
        -------
        str:
            Path containing run outputs.
        """
        raise NotImplementedError

    def get_num_runs(self, campaign=None, sampler=None, status=None, not_status=None):
        """
        Returns the number of runs matching the filtering criteria.

        Parameters
        ----------
        campaign: int or None
            Campaign id to filter for.
        sampler: int or None
            Sampler id to filter for.
        status: enum(Status) or None
            Status string to filter for.
        not_status: enum(Status) or None
            Exclude runs with this status string

        Returns
        -------
        int:
            The number of runs in the database matching the filtering criteria

        """

        raise NotImplementedError

    def get_campaign_id(self, name):
        raise NotImplementedError

    def get_run_status(self, run_name, campaign=None, sampler=None):
        raise NotImplementedError

    def set_run_statuses(self, run_ID_list, status):
        raise NotImplementedError

    def append_collation_dataframe(self, df):
        raise NotImplementedError

    def get_collation_dataframe(self):
        raise NotImplementedError

