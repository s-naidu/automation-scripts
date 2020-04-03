import connection


def exe_query(db_connection):
    cursor = db_connection.cursor()
    sql_create = """CREATE TABLE `ROLLBACK-DISTRO-2829_youtube_channel_video_status` AS
    SELECT * FROM youtube_channel_video_status
    WHERE youtube_video_id IN (
        'SikY0kfswqk', 'HqrTQL2T5Dc', 'AGr_Yv1bFtY', 'iP-IDpUrOFs',
        'taRZ4yxGepo', '0PbFKx28p_U', 'oezMCfuz2F0', 'upeoY2UqEAI',
        'GZdLxt0pNfg', 'OnfxS091OtQ', 'k-jtR6PDbSs', 'EXF_lBUPbGE',
        'qxqKh3iRoh8', 'rWKB5bRxG4c', 'S9ffqEOpf7w', 'd-Q_2GAQNzA',
        'V1DH474tdJw', 'xKDcJRPBqQo', '94mUF14L5lI', 'dCUqoF0QB-c',
        'Cwt_TjB6tS4', 'ahH4f-epe-k', 'laWN314XDyc', 'DHOI4_L5-qg',
        'ic3hp75iftM', 'mX-HU1hnNOc', '4Cvf_5KLkSA', '7hncS47R4z0',
        'Vl3q-1K5qwE', 'r1vct-qzoc0', '-ijuHYHYp4s', '6XDvya0cExQ',
        'KdVqgOn1ZLM', 'caJHa2Vf6nA', '2lsGniXPN70', 'WVP8UfIDnM4',
        'xpDSRYT0DXI', 'xpiJiF22z7w', 'vDlV1rTXmEI', 'bxACbPe_gok',
        'cUgJDEMnAS0', 'XZR9kxoWc1U', 'CVpPuViNBnE', 'FtsY8Q-QcjE',
        'luO_dSQEMeY', 'vpaRJEo9nPY', 'vJodE4ME-yI', 'f6RAdlQDguY',
        'u4TS6lTKS-0', '12Sd__hf6io', 'JPME3RKPGtk', 'RID8EY65ALY',
        'MmDfciIt_vI', 'orKaCJvXzU8', '8usKrNmCPEw', 'Neew1S7IJqM'
    ) """
    cursor.execute(sql_create)

    sql_delete = """DELETE yt.* FROM youtube_channel_video_status yt
    INNER JOIN `ROLLBACK-DISTRO-2829_youtube_channel_video_status`
    rp2829
        ON rp2829.youtube_video_id = yt.youtube_video_id"""
    cursor.execute(sql_delete)
    db_connection.commit()
    db_connection.close()


def main():
    db_connection = connection.database_connection()
    exe_query(db_connection)


if __name__ == '__main__':
    main()
